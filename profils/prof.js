import { useState, useEffect , useCallback} from "react";
import imageSrc from './react2.png'; // chemin vers l'image

import {
  Button,
  Form,
  Input,
} from "reactstrap";
import "./prof.css";

import React from 'react';


import "assets/css/nucleo-icons.css";
import "assets/scss/blk-design-system-react.scss";
import "assets/demo/demo.css";

export default function Général() {
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState("");
  const [text, setText] = useState(""); //texte alli yodhehr mil awel bel kol
  const [record, setRecord] = useState(false);
  const chaine = " *Espace Professeur"
  const [phrase, setPhrase] = useState("Bonjour, comment allez-vous ?");
  useEffect(() => {
    typeWriter(chaine);
    
  }, []);

  const typeWrit = (text) => {
    let i = 0;
    const speed = 100; // vitesse de frappe en ms
    const intervalId = setInterval(() => {
      if (i < text.length) {
        setText((prevText) => prevText + text.charAt(i));
        i++;
      } else {
        clearInterval(intervalId);
      }
    }, speed);
  };


  const handleSpeechRecognition = useCallback(() => {
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
      recognition.start();
    };

    recognition.start();

    return () => {
      recognition.stop();
    };
  }, []);

  

  //micro design

  /*const startRecording = () => {
    setRecord(true);
  };

  const stopRecording = () => {
    setRecord(false);
  };

  const onData = (recordedBlob) => {
    console.log('chunk of real-time data is: ', recordedBlob);
  };

  const onStop = (recordedBlob) => {
    console.log('recordedBlob is: ', recordedBlob);
  };*/

 


  //afficher l espace prof lettre par lettre
  const typeWriter = (text) => {
    let i = 0;
    const speed = 100; // vitesse de frappe en ms
    const intervalId = setInterval(() => {
      if (i < text.length) {
        setText((prevText) => prevText + text.charAt(i));
        i++;
      } else {
        clearInterval(intervalId);
      }
    }, speed);
  };

  const handleSubmit = useCallback(async () => {
    if (message) {
      // Send the message to your Flask backend
      const response = await fetch("http://localhost:5000/answerprof", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      console.log(data);
      setAnswer(data.answer);
    }
  }, [message]);

  useEffect(() => {
    handleSpeechRecognition();
  }, [handleSpeechRecognition]);

  useEffect(() => {
    const timeoutId = setTimeout(handleSubmit, 4000);
    return () => clearTimeout(timeoutId);
  }, [handleSubmit]);

  //prononcer
  useEffect(() => {
    const syntheseVocale = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(phrase);
    setTimeout(() => {
      syntheseVocale.speak(utterance);
    }, 5000);
  }, []);

  useEffect(() => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.stop();

    return () => {
      const newRecognition = new window.webkitSpeechRecognition();
      newRecognition.stop();
    };
  }, []);

//particles







  return (
   
    <div  className="hello">


      <div style={{ position: "relative", height: "100vh" }}>
      
        <h1 className="espace" style={{ marginTop: "100px", color: '#E1DBBD', fontSize: "250", marginLeft: "-450px" , fontFamily: "Arial, sans-serif"}}><center>{text}</center></h1>
        <h2 style={{ 
           
          fontSize: '1.5rem', 
          marginBottom: '1rem', 
          textAlign: 'center',
          marginLeft: '-450px' 
        }}>
            Spécifier précisément votre choix:
            
        </h2>
     
        <Form onSubmit={handleSubmit}>

          <div id="voice-icon"></div>
          <div class="grid">
            <div class="input-container">
              <input
                type="text"
                id="search-input"
                placeholder="Posez votre question..."
                value={message}
                onChange={(event) => setMessage(event.target.value)}
              />
            </div>
            <div class="input-container">
            <input type="text" value={answer} readOnly id="answer-input"/>
            </div>
          </div>
        
          <img src={imageSrc} 

            style={{
            width: "50%", // Changer la largeur de l'image à 50%
            position: "absolute", // Changer la position de l'image en absolu
            top: "50%", // Positionner l'image à 50% du haut de l'écran
            left: "73%", // Positionner l'image à 50% de la gauche de l'écran
            transform: "translate(-50%, -50%)", // Centrer l'image horizontalement et verticalement
            opacity: 0.5 // Changer l'opacité de l'image à 50%
          }}
          />


       

        


          <div className="container">
            <div className="wave-container">
              <div className="wave"></div>
            </div>

          </div>
        </Form>
      
      </div>




    </div>
    
    
  );
}