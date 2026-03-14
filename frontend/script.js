async function runAgent() {

    const task = document.getElementById("taskInput").value;
    const responseBox = document.getElementById("response");

    if (!task) {
        alert("Please enter a task");
        return;
    }

    responseBox.innerText = "Agent is working...";

    try {

        const response = await fetch("http://localhost:8000/run-agent", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                task: task,
                user_id: "user1"
            })
        });

        const data = await response.json();

        responseBox.innerText = JSON.stringify(data, null, 2);

        // If agent asks user for info
        if (data.status === "waiting_for_user") {

            const answer = prompt(data.question);

            if (answer) {
                sendUserAnswer(answer);
            }

        }

    } catch (error) {

        responseBox.innerText = "Error: " + error;

    }

}


async function sendUserAnswer(answer) {

    const responseBox = document.getElementById("response");

    responseBox.innerText = "Sending user input...";

    try {

        const response = await fetch("http://localhost:8000/user-input", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                answer: answer,
                user_id: "user1"
            })
        });

        const data = await response.json();

        responseBox.innerText = JSON.stringify(data, null, 2);

    } catch (error) {

        responseBox.innerText = "Error: " + error;

    }

}
