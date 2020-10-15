$(function () {
  var INTERVAL = 5000;

  // Object Urls
  var userSelf = '';
  var chatroomID = 'mainchat';
  var lastMessageID = '';
  var updateLock = false;

  // Backend API URLs
  var baseUrl = 'http://127.0.0.1:5000/';
  var createMessageUrl = `${baseUrl}messages/`;
  var refreshMessagesUrl = `${baseUrl}chat/${chatroomID}/updates`;
  var initMessagesUrl = `${baseUrl}chat/${chatroomID}/last`;
  var sessionTokenUrl = `${baseUrl}session/`;

  // jQuery Variables
  var $messages, $messageInput;
  $messages = $('#message-list');
  $messageInput = $('#message-input');

  $messageInput.on('submit', function (e) {
    e.preventDefault();
    var text = $('input:text').val();
    postMessage(text);
    $('input:text').val('');
    scrollChatToBottom();
  });

  function scrollChatToBottom() {
    $("#chat-window").animate({
      scrollTop: $('#chat-window').prop("scrollHeight")
    }, 1000);
  }

  // Create new message in this channel in backend
  function postMessage(text) {
    requestBody = {
      username: userSelf,
      chat_id: chatroomID,
      content: text
    }
    console.log(requestBody);
    $.ajax({
      type: "POST",
      url: createMessageUrl,
      data: JSON.stringify(requestBody),
      dataType: 'json',
      contentType: "application/json",
      success: function (data) {
        refreshMessages();
      }
    });
  }

  // Poll for new messages
  function refreshMessages() {
    if (updateLock) {
      return
    } else {
      updateLock = true;
      refreshUrl = refreshMessagesUrl + '?ref_id=' + lastMessageID.toString();
      $.ajax({
        type: "GET",
        url: refreshUrl,
        success: function (data) {
          renderMessages(data['messages']);
          updateLock = false;
        },
        error: function () {
          updateLock = false;
        }
      });
    }
  }

  // Logic needed to load page and initial messages
  function initPage() {
    var urlParams = new URLSearchParams(window.location.search);
    var token = urlParams.get('token');
    var urlWithToken = sessionTokenUrl + token + '/username/'
    $.ajax({
      type: "GET",
      url: urlWithToken,
      success: function (data) {
        username = data['username'];
        userSelf = username;
        initMessages();
      },
      error: function () {
        $('#content').replaceWith("<h1>Something Went Wrong</h1>");
      }
    })
  }

  // Load initial messages
  function initMessages() {
    $.ajax({
      type: "GET",
      url: initMessagesUrl,
      success: function (data) {
        if (data['messages'].length == 0) {
          lastMessageID = 0;
        }
        renderMessages(data['messages']);
        scrollChatToBottom();
      }
    });
  }

  // Add HTML to display new messages
  function renderMessages(messages) {
    messages.forEach(function (message) {
      if (message['username'] === userSelf) {
        $messages.append(`<li class="own-message"><div class="message-box">${message['content']}</div></li>`);
      } else {
        $messages.append(`<div>${message['username']}</div><li class="participant-message"><div class="message-box">${message['content']}</div></li>`);
      }
      lastMessageID = message['id'];
    });
    // scroll to bottom if there were new messages
    if (messages.length > 0) {
      scrollChatToBottom();
    }
  }

  initPage();

  // Continuously run refreshMessages at a certain interval
  setInterval(refreshMessages, INTERVAL);
});