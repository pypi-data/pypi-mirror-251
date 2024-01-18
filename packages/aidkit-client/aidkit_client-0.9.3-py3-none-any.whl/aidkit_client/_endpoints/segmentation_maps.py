from io import BytesIO
from typing import List

from numpy import asarray, uint8
from PIL import Image

from aidkit_client._endpoints.models import SegmentationMapResponse
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.exceptions import ResourceWithIdNotFoundError


class SegmentationMapAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def create(
        self,
        observation_id: int,
        segmentation_map_data: List[List[int]],
        class_names: List[str],
    ) -> SegmentationMapResponse:
        segmentation_map_bytes = BytesIO()
        Image.fromarray(asarray(segmentation_map_data, uint8)).save(segmentation_map_bytes, "PNG")

        return SegmentationMapResponse(
            **(
                await self.api.post_multipart_data(
                    path=f"/observation/{observation_id}/segmentation_map",
                    data={
                        "class_names": class_names,
                    },
                    files={
                        "segmentation_map_data": (
                            f"segmentation_map_{observation_id}",
                            segmentation_map_bytes.getvalue(),
                        )
                    },
                )
            ).body_dict_or_error(
                f"Failed to create segmentation map for observation {observation_id}."
            )
        )

    async def get_by_observation_id(self, observation_id: int) -> SegmentationMapResponse:
        result = await self.api.get(
            path=f"observation/{observation_id}/segmentation_map", parameters=None
        )
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(
                f"Segmentation map for observation with id {observation_id} not found"
            )
        return SegmentationMapResponse(
            **result.body_dict_or_error(
                f"Error fetching Segmentation map for observation with id {observation_id}."
            )
        )
