from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Room, Message


# =========================
# CHAT PAGE
# =========================
@login_required
def chat_page(request, room_id):

    room = get_object_or_404(Room, id=room_id)

    # mark seen messages
    Message.objects.filter(
        room=room,
        is_seen=False
    ).exclude(
        sender=request.user
    ).update(is_seen=True)

    messages = Message.objects.filter(room=room).order_by("timestamp")

    return render(request, "chat.html", {
        "room": room,
        "messages": messages
    })


# =========================
# START CHAT
# =========================
@login_required
def start_chat(request, user_id):

    other_user = get_object_or_404(User, id=user_id)

    room = Room.objects.filter(
        user1=request.user,
        user2=other_user
    ).first()

    if not room:
        room = Room.objects.filter(
            user1=other_user,
            user2=request.user
        ).first()

    if not room:
        room = Room.objects.create(
            user1=request.user,
            user2=other_user
        )

    return redirect("chat", room_id=room.id)


# =========================
# EDIT MESSAGE
# =========================
@login_required
def edit_message(request, message_id):

    if request.method == "POST":

        msg = get_object_or_404(Message, id=message_id, sender=request.user)

        msg.message = request.POST.get("message")
        msg.is_edited = True
        msg.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


# =========================
# DELETE MESSAGE
# =========================
@login_required
def delete_message(request, message_id):

    if request.method == "POST":

        msg = get_object_or_404(Message, id=message_id, sender=request.user)

        msg.is_deleted = True
        msg.message = "🚫 This message was deleted"

        if msg.image:
            msg.image.delete(save=False)
            msg.image = None

        msg.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


# =========================
# UPLOAD IMAGE
# =========================
@login_required
def upload_image(request, room_id):

    if request.method == "POST":

        room = get_object_or_404(Room, id=room_id)
        image = request.FILES.get("image")

        if image:
            Message.objects.create(
                room=room,
                sender=request.user,
                image=image,
                message_type="image"
            )

            return JsonResponse({"success": True})

    return JsonResponse({"success": False})


# =========================
# CHAT LIST (OPTIMIZED)
# =========================
@login_required
def chat_list(request):

    rooms = Room.objects.filter(user1=request.user) | Room.objects.filter(user2=request.user)
    rooms = rooms.distinct()

    chat_data = []

    for room in rooms:

        # latest message (FAST FIX)
        last_msg = Message.objects.filter(room=room).order_by("-timestamp").first()

        # unread count
        unread_count = Message.objects.filter(
            room=room,
            is_seen=False
        ).exclude(sender=request.user).count()

        # other user
        other_user = room.user2 if room.user1 == request.user else room.user1

        chat_data.append({
            "room": room,
            "user": other_user,
            "last_message": (
                last_msg.message if last_msg and last_msg.message
                else "📷 Image"
            ) if last_msg else "Start conversation...",
            "last_time": last_msg.timestamp if last_msg else room.created_at,
            "unread": unread_count
        })

    # 🔥 IMPORTANT: WhatsApp style sorting
    chat_data.sort(
        key=lambda x: x["last_time"],
        reverse=True
    )

    return render(request, "chat_list.html", {
        "chats": chat_data
    })