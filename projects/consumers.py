from channels.generic.websocket import AsyncJsonWebsocketConsumer

from projects.models import Project


class ProjectConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.project_pk = self.scope['url_route']['kwargs']['project_pk']
        self.project_group_name = f"project_{self.project_pk}"
        self.user = self.scope['user']

        if self.user.is_authenticated and self.is_project_member():
            await self.channel_layer.group_add(self.project_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.project_group_name, self.channel_name)


    async def receive_json(self, content, **kwargs):
        print(f"Received from {self.user.username}: {content}")


    def is_project_member(self):
        project = Project.objects.get(pk=self.project_pk)
        return project.members.filter(id=self.user.id).exists()