from typing import List, Optional, Dict, Union
from threading import Thread, Lock
import json
from pydantic import BaseModel, Field
from langchain_core.language_models import BaseChatModel

from deepeval.test_case import LLMTestCase
from deepeval.metrics import BaseMetric
from deepeval.utils import trimToJson
from deepeval.models import GPTModel
from deepeval.templates import FaithfulnessTemplate
from deepeval.progress_context import metrics_progress_context


class FaithfulnessVerdict(BaseModel):
    verdict: str
    reason: str = Field(default=None)
    truth: str = Field(default=None)


class FaithfulnessMetric(BaseMetric):
    def __init__(
        self,
        threshold: float = 0.5,
        model: Optional[Union[str, BaseChatModel]] = None,
        include_reason: bool = True,
    ):
        self.threshold = threshold
        # Don't set self.chat_model when using threading
        self.model = model
        self.include_reason = include_reason

    def measure(self, test_case: LLMTestCase):
        if (
            test_case.input is None
            or test_case.actual_output is None
            or test_case.retrieval_context is None
        ):
            raise ValueError(
                "Input, actual output, or retrieval context cannot be None"
            )
        with metrics_progress_context(self.__name__):
            self.truths_list: List[List[str]] = self._generate_truths_list(
                test_case.retrieval_context
            )
            self.verdicts_list: List[
                List[FaithfulnessVerdict]
            ] = self._generate_verdicts_list(
                self.truths_list, test_case.actual_output
            )
            faithfulness_score = self._generate_score()
            self.reason = self._generate_reason(faithfulness_score)
            self.success = faithfulness_score >= self.threshold
            self.score = faithfulness_score
            return self.score

    def _generate_score(self):
        total_verdicts = 0
        faithful_count = 0
        for verdicts in self.verdicts_list:
            total_verdicts += len(verdicts)
            for verdict in verdicts:
                if verdict.verdict.strip().lower() != "no":
                    faithful_count += 1

        return faithful_count / total_verdicts

    def _generate_reason(self, score: float):
        if self.include_reason is False:
            return None

        contradictions = []
        for index, verdicts in enumerate(self.verdicts_list):
            for verdict in verdicts:
                if verdict.verdict.strip().lower() == "no":
                    data = {"contradiction": verdict.reason, "rank": index + 1}
                    contradictions.append(data)

        prompt: dict = FaithfulnessTemplate.generate_reason(
            contradictions=contradictions,
            score=format(score, ".2f"),
        )

        chat_model = GPTModel(model=self.model)
        res = chat_model(prompt)
        return res.content

    def _generate_truths(
        self,
        context: str,
        chat_model: GPTModel,
        truths_list: List[str],
        lock: Lock,
    ):
        prompt = FaithfulnessTemplate.generate_truths(text=context)
        res = chat_model(prompt)
        json_output = trimToJson(res.content)
        data = json.loads(json_output)
        truths = data["truths"]

        with lock:
            truths_list.append(truths)

    def _generate_truths_list(
        self, retrieval_context: List[str]
    ) -> List[List[str]]:
        truths_list: List[List[str]] = []
        chat_model = GPTModel(model=self.model)
        threads = []
        lock = Lock()

        for context in retrieval_context:
            thread = Thread(
                target=self._generate_truths,
                args=(context, chat_model, truths_list, lock),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return truths_list

    def _generate_verdicts(
        self,
        truths: List[str],
        text: str,
        chat_model: GPTModel,
        verdicts_list: List[List[FaithfulnessVerdict]],
        lock: Lock,
    ):
        prompt = FaithfulnessTemplate.generate_verdicts(
            truths=truths, text=text
        )

        res = chat_model(prompt)

        json_output = trimToJson(res.content)
        data = json.loads(json_output)
        verdicts = [FaithfulnessVerdict(**item) for item in data["verdicts"]]

        if len(verdicts) != len(truths):
            raise ValueError(
                "Number of verdicts generated does not equal truths."
            )

        for i in range(len(verdicts)):
            verdicts[i].truth = truths[i]

        with lock:
            verdicts_list.append(verdicts)

    def _generate_verdicts_list(
        self, truths_list: List[List[str]], text: str
    ) -> List[List[FaithfulnessVerdict]]:
        verdicts_list: List[List[FaithfulnessVerdict]] = []
        chat_model = GPTModel(model=self.model)
        threads = []
        lock = Lock()

        for truths in truths_list:
            thread = Thread(
                target=self._generate_verdicts,
                args=(truths, text, chat_model, verdicts_list, lock),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return verdicts_list

    def is_successful(self) -> bool:
        self.success = self.score >= self.threshold
        return self.success

    @property
    def __name__(self):
        return "Faithfulness"
