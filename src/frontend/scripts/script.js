document.addEventListener("DOMContentLoaded", function () {
    const lightbox = document.getElementById("lightbox");
    const lightboxImage = document.querySelector(".lightbox-image");
    const lightboxTriggers = document.querySelectorAll(".lightbox-trigger");

    lightboxTriggers.forEach(trigger => {
        trigger.addEventListener("click", function () {
            const imageUrl = this.src;
            lightboxImage.src = imageUrl;
            lightbox.style.display = "flex";
        });
    });
});

function closeLightbox() {
    const lightbox = document.getElementById("lightbox");
    lightbox.style.display = "none";
}

function toggleCode(contentId) {
    var codeContent = document.getElementById(contentId);
    var computedStyle = window.getComputedStyle(codeContent);
    var maxHeight = computedStyle.getPropertyValue('max-height');

    // Get the actual height of the code snippet content
    var actualHeight = codeContent.scrollHeight;

    // Toggle between '0' and the actual height value
    codeContent.style.maxHeight = maxHeight === '0px' ? actualHeight + 'px' : '0';
}


  function toggleText(textId) {
    console.log("hello");
      var textContent = document.getElementById(textId).getElementsByClassName('text-content')[0];
      console.log(textContent);
      textContent.classList.toggle('expanded');
  }

async function runClassifierOne(dropdownId, consoleId, codeBlockId) {
    const parameter = document.getElementById(dropdownId).value;
    const consoleDiv = document.getElementById(consoleId);
    const codeBlock = document.getElementById(codeBlockId);
    // Clear previous logs
    consoleDiv.innerHTML = '';
    
    await delay(1000); // Adjust the delay time as needed


    consoleDiv.style.display = 'block';

    const originalLog = console.log;
      console.log = function(message) {
        originalLog.apply(console, arguments);
        const logMessage = document.createElement('p');
        logMessage.textContent = message;
        consoleDiv.appendChild(logMessage);
      };

    // Run the classifier logic
    classifyOne(parameter);

    // Restore the original console.log function
    console.log = originalLog;
  }

  // Replace this with the actual classifier logic
  function classifyOne(parameter) {
    const sunnyStittMargin = 25.770;
    const sunnyRollinsMargin = 1.688;
    const eternalStittMargin = 198.652;
    const eternalRollinsMargin = 94.270;
    // Your classifier logic here
    if (parameter === 'sunny stitt') {
        console.log(`>> LL(Stitt) = -1009.76`);
        console.log(`>> LL(Rollins) = -1035.53`);
        console.log(`>> It is most likely to have been played by Stitt, with a margin of ${sunnyStittMargin}`);
      } else if (parameter === 'sunny rollins') {
        console.log(`>> LL(Stitt) = -780.79`);
        console.log(`>> LL(Rollins) = -779.10`);
        console.log(`>> It is most likely to have been played by Rollins, with a margin of ${sunnyRollinsMargin}`);
      } else if (parameter === 'eternal stitt') {
        console.log(`>> LL(Stitt) = -2331.18`);
        console.log(`>> LL(Rollins) = -2529.83`);
        console.log(`>> It is most likely to have been played by Stitt, with a margin of ${eternalStittMargin}`);
      } else if (parameter === 'eternal rollins') {
        console.log(`>> LL(Stitt) = -2246.96`);
        console.log(`>> LL(Rollins) = -2341.23`);
        console.log(`>> It is most likely to have been played by Stitt, with a margin of ${eternalRollinsMargin}`);
      } else {
        console.log(parameter);
      }
  }

  async function runClassifierTwo(dropdownId, consoleId, codeBlockId) {
    const parameter = document.getElementById(dropdownId).value;
    const consoleDiv = document.getElementById(consoleId);
    const codeBlock = document.getElementById(codeBlockId);


    // Clear previous logs
    consoleDiv.innerHTML = '';
    
    await delay(1500); // Adjust the delay time as needed

    

    consoleDiv.style.display = 'block';

    const originalLog = console.log;
      console.log = function(message) {
        originalLog.apply(console, arguments);
        const logMessage = document.createElement('p');
        logMessage.textContent = message;
        consoleDiv.appendChild(logMessage);
      };

    // Run the classifier logic
    classifyTwo(parameter);

    // Restore the original console.log function
    console.log = originalLog;
  }

  // Replace this with the actual classifier logic
  function classifyTwo(parameter) {
    // Your classifier logic here
    if (parameter === 'sunny stitt') {
        console.log(`>> It is most likely that Stitt was first and Rollins was second`);
      } else if (parameter === 'sunny rollins') {
        console.log(`>> It is most likely that Rollins was first and Stitt was second`);
      } else if (parameter === 'eternal stitt') {
        console.log(`>> It is most likely that Stitt was first and Rollins was second`);
      } else if (parameter === 'eternal rollins') {
        console.log(`>> It is most likely that Rollins was first and Stitt was second`);
      } else {
        console.log(parameter);
      }
  }

  function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

var coll = document.getElementsByClassName("collapsible");
var i;

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}