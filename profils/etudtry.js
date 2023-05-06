import { useState, useEffect , useCallback} from "react";

import {
  Button,
  Label,
  Form,
  FormGroup,
  CustomInput,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  Container,
  Row,
  Col
} from "reactstrap";
import React from "react";

export default function Général() {
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState('')

  const handleSpeechRecognition =  useCallback(() => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "fr-FR";

    recognition.onstart = () => {
      console.log("Speech recognition started");
    };

    recognition.onresult = (event) => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      setMessage(finalTranscript);
    };

    recognition.onerror = (event) => {
      console.error(event.error);
    };

    recognition.onend = () => {
      console.log("Speech recognition ended");
      handleSpeechRecognition();
    };

    recognition.start();
  },[]);
  //Définissez une nouvelle fonction qui prendra la réponse en tant qu'argument et la prononcera à haute voix en utilisant l'API SpeechSynthesis
  function speak(answer) {
    const utterance = new SpeechSynthesisUtterance(answer);
    speechSynthesis.speak(utterance);
  }

 
  //const handleSubmit = useCallback(async () => {
    //if (message) {
    // Send the message to your Flask backend
    //const response = await fetch("http://localhost:5000/answeretud", {
      //method: "POST",
      //headers: {
        //"Content-Type": "application/json",
      //},
      //body: JSON.stringify({ message }),
    //});
  
    //const data = await response.json();
    //console.log(data);
    //setAnswer(data.answer)}
  
  //}, [message]);


  //modifier handle
  const handleSubmit = useCallback(async () => {
    if (message) {
      // Send the message to your Flask backend
      const response = await fetch("http://localhost:5000/answeretud", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
  
      const data = await response.json();
      console.log(data);
      setAnswer(data.answer);
  
      // Call speak function to pronounce the answer
      speak(data.answer);
    }
  }, [message]);
  

  useEffect(() => {
    handleSpeechRecognition();
  }, [handleSpeechRecognition]);

useEffect(() => {
  const timeoutId = setTimeout(handleSubmit, 4000);
  return () => clearTimeout(timeoutId);
}, [handleSubmit]);
  return (
    <div>
      <h1 style={{ marginTop: "80px" }}>ESPACE Etudiant</h1>
      <h2>Spécifier precisemment votre choix:</h2>
      <div>
      <Form /*  onSubmit={handleSubmit} */>
        <Input
          type="text"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
        />
       
     
      <Input
          type="text"
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
          disabled
        />  
         <Button type="submit">Send</Button>

         
        </Form>
        <p>{answer}</p>
      </div>
    </div>
  );
}