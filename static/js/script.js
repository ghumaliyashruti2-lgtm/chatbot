function sendQuick(text){
  sendToChat(text);
  botReply(text);
}

function sendMessage() {
  let input = document.getElementById("userInput");
  if (input.value.trim() == "") return;
  sendToChat(input.value);
  botReply(input.value);
  input.value = "";
}

function sendToChat(text){
  let chatBody = document.getElementById("chatBody");
  let userMsg = document.createElement("div");
  userMsg.classList.add("user-message");
  userMsg.innerText = text;
  chatBody.appendChild(userMsg);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// ----------------------
// BOT REPLY LOGIC
// ----------------------

function botReply(text){
  let lower = text.toLowerCase();

  if(lower.includes("course")){
    showCourseButtons();
  }
  else {
    let reply = "";

    if(lower.includes("fees"))
      reply = "Course fees start from ₹4,999 to ₹24,999 depending on module.";
    else if(lower.includes("duration"))
      reply = "Course duration varies 4–12 weeks.";
    else if(lower.includes("location") || lower.includes("contact"))
      reply = "Nana Varachha, Surat • +91 87805 62404";
    else if(lower.includes("job"))
      reply = "We provide placement support after course completion.";
    else
      reply = "Thank you! Our team will assist you shortly 😊";

    showBotMessage(reply);
  }
}

// ----------------------
// SHOW NORMAL BOT TEXT
// ----------------------

function showBotMessage(text){
  setTimeout(()=>{
    let chatBody = document.getElementById("chatBody");
    let botMsg = document.createElement("div");
    botMsg.classList.add("bot-message");
    botMsg.innerText = text;
    chatBody.appendChild(botMsg);
    chatBody.scrollTop = chatBody.scrollHeight;
  }, 400);
}

// ----------------------
// SHOW COURSE BUTTONS
// ----------------------

function showCourseButtons(){
  setTimeout(()=>{
    let chatBody = document.getElementById("chatBody");

    const courses = [
      "Python",
      "Java",
      "Full Stack",
      "Web Development",
      "More"
    ];

    let box = document.createElement("div");
    box.classList.add("course-options-box");

    courses.forEach(course => {
      let btn = document.createElement("button");
      btn.classList.add("smart-option-btn");
      btn.innerText = course;

      btn.addEventListener("click", () => {
        sendToChat(course);
        botReply(course);
      });

      box.appendChild(btn);
    });

    chatBody.appendChild(box);
    chatBody.scrollTop = chatBody.scrollHeight;

  }, 400);
}


// country and city name and mobile code 


const data = {

    "India": {
        code: "+91",
        cities: [
            "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Mumbai", "Pune",
            "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata",
            "Jaipur", "Lucknow", "Kanpur", "Indore", "Bhopal", "Agra"
        ]
    },

    "United States": {
        code: "+1",
        cities: [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "San Diego", "Dallas", "San Jose", "Philadelphia"
        ]
    },

    "United Kingdom": {
        code: "+44",
        cities: [
            "London", "Manchester", "Birmingham", "Liverpool", "Leeds",
            "Bristol", "Sheffield"
        ]
    },

    "Canada": {
        code: "+1",
        cities: [
            "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa",
            "Edmonton"
        ]
    },

    "Australia": {
        code: "+61",
        cities: [
            "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"
        ]
    },

    "Germany": {
        code: "+49",
        cities: [
            "Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"
        ]
    }

    

    
};



let countryDropdown = document.getElementById("country");
for (let country in data) {
    countryDropdown.innerHTML += `<option value="${country}">${country}</option>`;
}



document.getElementById("country").addEventListener("change", function () {
    let selected = this.value;
    let mobile = document.getElementById("mobile");
    let city = document.getElementById("city");

    if (selected && data[selected]) {
        // Set mobile code
        mobile.value = data[selected].code + " ";

        // Fill cities
        city.innerHTML = "<option value=''>Select City</option>";
        data[selected].cities.forEach(c => {
            city.innerHTML += `<option value="${c}">${c}</option>`;
        });

    } else {
        mobile.value = "";
        city.innerHTML = "<option value=''>Select City</option>";
    }
});

// image show on edit page

function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        const img = document.getElementById("previewImg");
        img.src = URL.createObjectURL(file);
        img.style.display = "block";
    }
}

