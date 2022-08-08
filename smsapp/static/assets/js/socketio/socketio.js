// jQuery (necessary for Bootstrap's JavaScript plugins)
document.addEventListener("DOMContentLoaded", () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/?room_id=' + room_id );

    // Create event buckets
    socket.on("connect", () => {
        socket.emit("join_chat", {
            "room_id": room_id,
        });
        scrollDownChatWindow()
    })

    // Message Event
    socket.on('message', data => {
        // Display messages
        if (data['message']) {
            if (data.username == username ) {
                document.querySelector("#users-conversation").
                insertAdjacentHTML("beforeend", `<li class="chat-list right" id="1">
                <div class="conversation-list">
                    <div class="chat-avatar"><img src="/static/assets/images/users/${data['sender_image']}" alt="">
                    </div>
                    <div class="user-chat-content">
                        <div class="ctext-wrap">
                            <div class="ctext-wrap-content" id="1">
                                <p class="mb-0 ctext-content">${data['message']}</p>
                            </div>
                            <div class="dropdown align-self-start message-box-drop"> <a
                                    class="dropdown-toggle" href="#" role="button"
                                    data-bs-toggle="dropdown" aria-haspopup="true"
                                    aria-expanded="false"> <i class="ri-more-2-fill"></i> </a>
                                <div class="dropdown-menu"> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between reply-message"
                                        href="#" id="reply-message-0" data-bs-toggle="collapse"
                                        data-bs-target=".replyCollapse">Reply <i
                                            class="bx bx-share ms-2 text-muted"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between"
                                        href="#" data-bs-toggle="modal"
                                        data-bs-target=".forwardModal">Forward <i
                                            class="bx bx-share-alt ms-2 text-muted"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between copy-message"
                                        href="#" id="copy-message-0">Copy <i
                                            class="bx bx-copy text-muted ms-2"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between"
                                        href="#">Bookmark <i
                                            class="bx bx-bookmarks text-muted ms-2"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between"
                                        href="#">Mark as Unread <i
                                            class="bx bx-message-error text-muted ms-2"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between delete-item"
                                        href="#">Delete <i
                                            class="bx bx-trash text-muted ms-2"></i></a> </div>
                            </div>
                        </div>
                        <div class="conversation-name"><small class="text-muted time">${data['timestamp']}
                                </small> <span class="text-success check-message-icon"><i
                                    class="bx bx-check-double"></i></span></div>
                    </div>
                </div>
            </li>`);
            }
            else if (typeof data.username !== username) {
                document.querySelector("#users-conversation").
                insertAdjacentHTML("beforeend", `<li class="chat-list left" id="1">
                <div class="conversation-list">
                    <div class="chat-avatar"><img src="/static/assets/images/users/${data['sender_image']}" alt="">
                    </div>
                    <div class="user-chat-content">
                        <div class="ctext-wrap">
                            <div class="ctext-wrap-content" id="1">
                                <p class="mb-0 ctext-content">${data['message']}</p>
                            </div>
                            <div class="dropdown align-self-start message-box-drop"> <a
                                    class="dropdown-toggle" href="#" role="button"
                                    data-bs-toggle="dropdown" aria-haspopup="true"
                                    aria-expanded="false"> <i class="ri-more-2-fill"></i> </a>
                                <div class="dropdown-menu"> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between reply-message"
                                        href="#" id="reply-message-0" data-bs-toggle="collapse"
                                        data-bs-target=".replyCollapse">Reply <i
                                            class="bx bx-share ms-2 text-muted"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between"
                                        href="#" data-bs-toggle="modal"
                                        data-bs-target=".forwardModal">Forward <i
                                            class="bx bx-share-alt ms-2 text-muted"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between copy-message"
                                        href="#" id="copy-message-0">Copy <i
                                            class="bx bx-copy text-muted ms-2"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between"
                                        href="#">Bookmark <i
                                            class="bx bx-bookmarks text-muted ms-2"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between"
                                        href="#">Mark as Unread <i
                                            class="bx bx-message-error text-muted ms-2"></i></a> <a
                                        class="dropdown-item d-flex align-items-center justify-content-between delete-item"
                                        href="#">Delete <i
                                            class="bx bx-trash text-muted ms-2"></i></a> </div>
                            </div>
                        </div>
                        <div class="conversation-name"><small class="text-muted time">${data['timestamp']}
                                </small> <span class="text-success check-message-icon"><i
                                    class="bx bx-check-double"></i></span></div>
                    </div>
                </div>
                </li>`);
            }
        }

        scrollDownChatWindow(); 
    });

    

    // Event joined_chat
    socket.on('joined_chat', data => {
        console.log("User has joined the room\n\n\n\n\n\n")
    })

    var form = $('#chatinput-form').on('submit', function (e) {
        e.preventDefault();

        // Send message to user through outgoing messages event
        socket.emit(
            "outgoing",
            {
                'message': document.querySelector("#chat-inputs").value,
                'sender_image': sender_image,
                'room_id': room_id,
                'username': username
            }
        );
        // Clear input area
        document.querySelector("#chat-inputs").value = ""
        scrollDownChatWindow()
    })
    
    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#chat-conversation .simplebar-content-wrapper");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
    
})

