const form = document.querySelector('.form');
const messagesDiv = document.querySelector('.messages');
const scoreElement = document.querySelector('#game-score');
const timerElement = document.querySelector('#timer');
const startButton = document.querySelector('#start-button');

let started = false;
let time = 60; // seconds
let score = 0; // points

function updateGameScore(score){
    scoreElement.innerText = `Score: ${score}`;
}

function updateTimer(second){
    timerElement.innerText = `Time: ${second}`;
}

function startTimer(seconds){ // timer function I stole from a previous exercise of mine
    let timer = setInterval(() => {
        seconds--;
        if(seconds <= 0){
            clearInterval(timer);
            sendMessage('PM', `Game is over, you scored ${scoreElement.innerText}!`);
            started = false // stops player from being able to click submit button
        }
        else{
            console.log(seconds);
        }
        updateTimer(seconds);
    }, 1000);
}

function sendMessage(result, personalMessage="", classname='notification'){ // classnames can range from notification, to success, or failure
    messagesDiv.innerHTML = '';
    const message = document.createElement('h1');

    if (result == 'PM'){
        message.append(personalMessage);
        messagesDiv.classList.toggle(classname);
        messagesDiv.append(message);
        return;
    }

    if (result == 'ok'){
        message.append('Word is on board, that\'s a point!');
        messagesDiv.classList.toggle('success');
    }
    else if (result == 'not-word'){
        message.append('Word is on board, but it\'s not a word.');
        messagesDiv.classList.toggle('notification');
    }
    else if(result == 'already-submitted'){
        message.append('Word is on board, but you already submitted it.');
        messagesDiv.classList.toggle('failure');
    }
    // result == 'not-on-board'
    else{
        message.append('Word is not on board.');
        messagesDiv.classList.toggle('failure');
    }
    messagesDiv.append(message);

}

/* js frontend checks validity of word user submitted from form */
form.addEventListener('submit', async function checkWord(event){
    event.preventDefault();
    if (started){
        textBox = document.querySelector('#form-value');
        value = document.querySelector('#form-value').value;
        if (value.trim() == ''){
            console.log("You can't submit nothing!");
            sendMessage("PM", "You can't submit nothing!", 'failure')
        }
        else{
            const result = await axios.get(`/post/${value}`);
            const isValidWord = result.data.valid_word;
            const score = result.data.game_score;
            if (score != undefined){
                updateGameScore(score)
            }
            textBox.value = '';
    
            sendMessage(isValidWord);
        }
    }
});

/* start timer and allow user to submit responses to game */
startButton.addEventListener('click', startGame);

function startGame(){
    startTimer(time);
    started = true
    console.log('TIMER HAS STARTED!');
    removeEventListener('click', startGame); // stops board from being pressed again, and timer getting all weird...
}
