"""
SQLAdmin - Views - Model View.
"""

from fastapi import Request
from sqladmin import ModelView


class CustomModelView(ModelView):
    """
    Custom Model View.
    """

    async def delete_model(self, request: Request, pk: int) -> None:
        """
        Handle deletion of the model.
        """

        model = self.model.query().filter_by(id=pk).first()

        if not model:
            return None

        if not model.deleted_at:
            model.delete()
        else:
            await super().delete_model(request, pk)

        return model
