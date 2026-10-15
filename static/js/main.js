// رفتارهای ساده سمت کلاینت.
// اتصال WebSocket برای بخش گفتگو (chat) در آینده اینجا اضافه می‌شود.

document.addEventListener("DOMContentLoaded", function () {
  var chatForm = document.getElementById("chat-form");
  if (chatForm) {
    chatForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = chatForm.querySelector('input[name="message"]');
      if (!input.value.trim()) return;

      var messages = document.getElementById("chat-messages");
      var bubble = document.createElement("div");
      bubble.className = "chat-bubble chat-bubble--me";
      bubble.textContent = input.value;
      messages.appendChild(bubble);
      messages.scrollTop = messages.scrollHeight;
      input.value = "";
    });
  }
});
