from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Tuple

from _qwak_proto.qwak.feature_store.sources.data_source_pb2 import (
    DataSourceSpec as ProtoDataSourceSpec,
)
from qwak.exceptions import QwakException
from qwak.feature_store._common.artifact_utils import ArtifactSpec, ArtifactsUploader
from qwak.feature_store.validations.validation_options import (
    DataSourceValidationOptions,
)
from qwak.feature_store.validations.validation_response import SuccessValidationResponse

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass


@dataclass
class BaseSource(ABC):
    name: str
    description: str

    @abstractmethod
    def _to_proto(self, artifact_url: Optional[str] = None) -> ProtoDataSourceSpec:
        pass

    def _get_artifacts(self) -> Optional["ArtifactSpec"]:
        return None

    def _upload_artifact(self) -> Optional[str]:
        artifact: Optional["ArtifactSpec"] = self._get_artifacts()
        if artifact:
            return ArtifactsUploader.upload(artifact)

    def _prepare_and_get(
        self, artifact_url: Optional[str] = None
    ) -> Tuple[ProtoDataSourceSpec, Optional[str]]:
        uploaded_artifact_url: Optional[str] = artifact_url

        if not artifact_url:
            uploaded_artifact_url = self._upload_artifact()

        proto_definition: ProtoDataSourceSpec = self._to_proto(
            artifact_url=uploaded_artifact_url
        )

        return proto_definition, uploaded_artifact_url

    @classmethod
    @abstractmethod
    def _from_proto(cls, proto):
        pass

    def get_sample(
        self,
        number_of_rows: int = 10,
        validation_options: Optional[DataSourceValidationOptions] = None,
    ) -> "pd.DataFrame":
        """
        Tries to get a sample of length `number_rows` from the data source.
        Args:
            number_of_rows: number of rows to get from data source
            validation_options: validation options
        Returns:
            A tuple containing the resulting dataframe and a tuple of the columns names and types.
            (the types are pyspark dataframe types)
        """
        from qwak.feature_store.validations.validator import FeaturesOperatorValidator

        v = FeaturesOperatorValidator()

        response, _ = v.validate_data_source(
            data_source=self,
            sample_size=number_of_rows,
            validation_options=validation_options,
        )

        if isinstance(response, SuccessValidationResponse):
            return response.sample
        else:
            raise QwakException(f"Sampling failed: \n{response}")
