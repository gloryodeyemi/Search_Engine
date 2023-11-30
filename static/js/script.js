$(function () {
    $("#search-input").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/autocomplete",
                data: { query: request.term },
                dataType: "json",
                success: function (data) {
                    response(data.suggestions);
                }
            });
        },
        minLength: 2, // minimum characters before the autocomplete activates
    });
});

document.getElementById('filter_type').addEventListener('change', function () {
    var selectedValue = this.value;
    var filterValueLabel = document.querySelector('#filter-value-container label');
    var filterValueInput = document.querySelector('#filter-value-container input');
    if (selectedValue === 'year' || selectedValue === 'year_range' || selectedValue === 'paper_type') {
        filterValueLabel.style.display = 'inline-block';
        filterValueInput.style.display = 'inline-block';
    } else {
        filterValueLabel.style.display = 'none';
        filterValueInput.style.display = 'none';
    }
});

var voiceSearchButton = document.getElementById('voice-search-btn');
var searchInput = document.getElementById('search-input');

voiceSearchButton.addEventListener('click', function(event) {
    event.preventDefault();
    startDictation();
});

function capitalize(s) {
    if (typeof s !== 'string') return '';
    return s.charAt(0).toUpperCase() + s.slice(1);
}

function linebreak(s) {
    return s.replace(/\n/g, '<br>');
}

function startDictation() {
    console.log("startDictation function is being called.");
    if (!('webkitSpeechRecognition' in window)) {
        upgrade();
    } else {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;

        recognition.onstart = function() {
            console.log("Recognition started.");
            voiceSearchButton.style.backgroundColor = "#ff0000"; // red color to indicate active listening
            voiceSearchButton.innerHTML = "Listening..."; // change the button text to indicate active listening
        };

        recognition.onresult = function(event) {
            console.log("Recognition results: ", event);
            searchInput.value = event.results[0][0].transcript;
        };

        recognition.onerror = function(event) {
            console.error("Recognition error: ", event);
            if (event.error === 'not-allowed') {
                console.log("Microphone access not allowed. Please enable the microphone.");
                alert("Microphone access is not allowed. Please enable the microphone in your browser settings.");
            }
            recognition.stop();
        };

        recognition.onend = function() {
            console.log("Recognition ended.");
            voiceSearchButton.innerHTML = "Voice search";
            recognition.stop();
        };

        // code for the start button
        recognition.lang = "en-US";
        recognition.start();
    }
}