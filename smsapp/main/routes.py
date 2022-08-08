from socket import socket
from time import localtime, time, strftime
from flask_login import current_user, login_required
from flask_socketio import send, emit, join_room, leave_room
from flask import redirect, render_template, request, url_for
from smsapp.main import main
from smsapp import socketio, db
from .forms import AddContactForm
from smsapp.models import User, Chat
import json

# Homepage route, this route redirects to login/register page
@main.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("auth.login"))


@main.route('/chat/', methods=["GET", "POST"])
@login_required
def chat_page():
    # Get the room id in the url
    room_id = request.args.get('room_id', None)
    form = AddContactForm()
    # Initialize data context for the template
    chat_data = []
    # Get all the chat list for logged in user
    chat_dict = {}
    messages = None
    recepient = None
    mychat = Chat.query.filter_by(user=current_user).all()
    if mychat:
        for i in mychat:
            # Load chat details from the database and store in chat_dict
            details = i.chat_details
            chat_dict.update(details)
    
    # Get all data from the chat list
    for k, v in chat_dict.items():
        contact_name = v['chat_name']
        messages = v['messages']
        recepient_image = v['recepient_image']
        # Append data to the chat data context
        chat_data.append(
            {
                'contact_name': contact_name,
                'messages': messages,
                'room_id': k, 
                'recepient_image': recepient_image,
            }
        )
        # Get all chat details
        # Get all message history
        chats = Chat.query.filter_by(room_id=room_id).first()
        if chats:
            # Get recepient details
            recepient = Chat.query.filter_by(room_id=room_id).filter(
                        Chat.user_id != current_user.id).first()
            # Message history
            for k, v in chats.chat_details.items():
                messages = v['messages']
    return render_template('main/index.html', title="Home Page", 
                           user_image=current_user.image,
                           username=current_user.username, form=form,
                           chat_data=chat_data, room_id=room_id, 
                           messages=messages, recepient=recepient)


# Adding new chat
@main.route('/new_chat', methods=['POST'])
def new_chat():
    # Get user id and new chat email
    user_id = current_user.id
    new_chat_email = request.form.get('email')
    new_chat_name = request.form.get('name')
    new_chat_message = request.form.get('message')
    # Prevent user from adding their self
    if new_chat_email == current_user.email:
        print("Can't add yourself")
        return redirect(url_for('main.chat_page'))
    # Check whether account has been registered
    if User.query.filter_by(email=new_chat_email).first() is None:
        print("User has not been registered")
        return redirect(url_for('main.chat_page'))
    try:
        # Prevent User from adding the same recepient twice
        pass
        recepient = User.query.filter_by(email=new_chat_email).first_or_404()
        # Add Chat details to the database
        # Generate unique room ID value
        room_id = str(recepient.username[-3:]+ current_user.username[-3:]+
                      (str(current_user.id) + str(recepient.id))[-3:]) 
        # Get the chat details of the user
        mychat_details = {
            room_id: {
                'chat_name': recepient.username,
                'chat_email': new_chat_email,
                'recepient_image': recepient.image,
                'messages': [],
            }
        }
        recepientchat_details = {
            room_id: {
                'chat_name': current_user.username,
                'chat_email': current_user.email,
                'recepient_image': current_user.image,
                'messages': [],
            }
        }
        mychat = Chat(user=current_user, recepient=recepient.username, 
                      room_id=room_id,
                      chat_details=mychat_details)
        recepient_chat = Chat(user=recepient, recepient=current_user.username, 
                              room_id=room_id,
                              chat_details=recepientchat_details)
        db.session.add(mychat)
        db.session.add(recepient_chat)
        db.session.commit()
        print("My new chat added")
        return redirect(url_for('main.chat_page'))
    except Exception as e:
        print(e, "This is the error message\n\n\n\n\n")
    
    
    
    return redirect(url_for('main.chat_page'))
    
    
@socketio.on('join_chat')
def join_chat(data):
    # Get the room ID
    room = data['room_id']
    join_room(room)
    # Send message to show that user has joined the room
    emit(
        "joined_chat",
        {
            'message': f"{room} has been joined",
        },
        room=room
    )

@socketio.on("outgoing")
def chatting_system(data):
    room_id = data['room_id'] 
    timestamp =  strftime('%b-%d %I:%M %p', localtime())
    message = {
        'timestamp': timestamp,
        'username': data['username'],
        'message': data['message'],
    }
    # username= data['username']
    conversation= {}
    
    # Update the message list of both users
    # User message list update
    mychat = Chat.query.filter_by(room_id=data['room_id']).\
            filter(Chat.user_id == current_user.id).first()
    myconversation = mychat.chat_details
    myconversation[room_id]['messages'].append(message)
    
    mychat_update = Chat.query.filter_by(room_id=data['room_id']).\
                    filter(Chat.user_id == current_user.id).\
                    update(dict(chat_details=myconversation))
    
    #Recepient message list update    
    recepient_chat = Chat.query.filter_by(room_id=data['room_id']).\
            filter(Chat.user_id != current_user.id).first()
    recepient_conversation = recepient_chat.chat_details
    recepient_conversation[room_id]['messages'].append(message)
    
    recepient_chat_update = Chat.query.filter_by(room_id=data['room_id']).\
                    filter(Chat.user_id != current_user.id).\
                    update(dict(chat_details=recepient_conversation))
    db.session.commit()
    
    # Emit message to users in the room
    emit(
        "message",
        {
            'message': data['message'],
            'timestamp': timestamp,
            'sender_image': data['sender_image'],
            'username': data['username']
        },
        room = room_id,
        
    )