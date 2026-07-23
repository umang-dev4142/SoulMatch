from django.urls import path

from .views import (
    chat_page,
    start_chat,
    edit_message,
    delete_message,
    upload_image,
    chat_list
)

urlpatterns = [
    path("chat/<int:room_id>/", chat_page, name="chat"),
    path("start-chat/<int:user_id>/", start_chat, name="start_chat"),
    path("edit-message/<int:message_id>/", edit_message, name="edit_message"),
    path("delete-message/<int:message_id>/", delete_message, name="delete_message"),
    path("upload-image/<int:room_id>/", upload_image, name="upload_image"),
    path("chats/", chat_list, name="chat_list"),
]