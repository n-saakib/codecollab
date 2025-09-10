from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from projects.models import Project, File


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
        """
        Called when we receive a message from the WebSocket.
        """
        message_type = content.get("type")
        if message_type == "editor_update":
            file_id = content.get("file_id")
            new_content = content.get("content")

            await self.save_file_content(file_id, new_content)

            await self.channel_layer.group_send(
                self.project_group_name,
                {
                    'type': 'editor_update_broadcast',
                    'file_id': file_id,
                    'content': new_content,
                    'sender_channel': self.channel_name
                }
            )

    async def editor_update_broadcast(self, event):
        """
        This method is called when an editor_update message is received from the group.
        It sends the message down to the client's WebSocket.
        """
        # Don't send the message back to the original sender
        if self.channel_name != event['sender_channel']:
            await self.send_json({
                'type': 'editor_update',
                'file_id': event['file_id'],
                'content': event['content']
            })


    @sync_to_async
    def is_project_member(self):
        project = Project.objects.get(pk=self.project_pk)
        return project.members.filter(id=self.user.id).exists()

    @sync_to_async
    def is_project_member(self):
        # ... (This method remains the same as before)
        project = Project.objects.get(pk=self.project_pk)
        return project.members.filter(id=self.user.id).exists()

    @sync_to_async
    def save_file_content(self, file_id, content):
        """
        Saves the file content to the database. Wrapped in sync_to_async.
        """
        try:
            # We only update the content field
            File.objects.filter(pk=file_id).update(content=content)
        except File.DoesNotExist:
            print("File not found")