import broom from "./broom.png";
import send from "./send.png";
import chatIcon from "./chatIcon.png";
import "./App.css";
import { useEffect, useRef, useState } from "react";
import OutfitCard from "./OutfitCard";
import UserMessage from "./UserMessage";

function App() {
  var countMessages = 0;
  const [outfitText, setOutfitText] = useState("");
  const messagesContainerRef = useRef(null);
  const [outfits, setOutfits] = useState([]);

  const [chatLog, setChatLog] = useState([]);

  useEffect(() => {
    if (chatLog.length) {
      console.log("Scroll to bottom ran", chatLog.length);

      messagesContainerRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "end",
      });
    }
  }, [chatLog.length]);

  const clearChat = async () => {
    try {
      const response = await fetch("http://192.168.248.92:8122/reset_chat");
      if (response.ok) {
        console.log("Chat Cleared");
      } else {
        console.error("Error fetching data:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  const handleSubmit = async (event) => {
    countMessages += 1;
    if (countMessages <= 5) {
      event.preventDefault();
      const currText = outfitText;
      setOutfitText("");
      const endpoint = "http://192.168.248.92:8122/get_outfit"; // Replace with your actual endpoint URL

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            credentials: "include",
          },
          body: JSON.stringify({ user_prompt: currText }),
        });

        if (response.ok) {
          // Handle successful response
          const data = await response.json();
          const currData = [
            {
              IsUser: true,
              UserPrompt: currText,
            },
            {
              IsUser: false,
              OutFits: data.outfit,
            },
          ];
          setChatLog((prevChats) => [...prevChats, ...currData]);
          setOutfits(data.outfit);

          console.log("Outfit search successful!");
        } else {
          console.error("Outfit search failed.");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    } else {
      event.preventDefault();
      const currText = outfitText;
      setOutfitText("");
      const endpoint = "http://192.168.248.92:8122/get_outfit";
      const currData = [
        {
          IsUser: false,
          OutFits: [],
        },
      ];
      setChatLog((prevChats) => [...prevChats, ...currData]);
    }
  };

  const handleOutfitTextChange = (event) => {
    setOutfitText(event.target.value);
  };
  const adjustTextareaHeight = (element) => {
    element.style.height = "auto";
    element.style.height = element.scrollHeight + "px";
  };

  const handleTextareaInput = (event) => {
    adjustTextareaHeight(event.target);
  };
  const handleTextAreaKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      handleSubmit(event);
    }
  };
  return (
    <div ref={messagesContainerRef} className="App">
      <h2 className="WelcomeText">
        Welcome to Neytiri: An outfit Avatar Generator!
      </h2>
      <div className="Container">
        {chatLog.map((Obj, index) => (
          <>
            {Obj.IsUser ? (
              <div className="PrevSearchText">
                <UserMessage message={Obj.UserPrompt} />
              </div>
            ) : (
              <div className="ImageContainer">
                {Obj.OutFits.length === 0 ? (
                  <div className="Card2">
                    Sorry, You have reached the free tier chat message limit of
                    this conversation, Kindly clear the chat or upgrade to a
                    better plan!
                  </div>
                ) : (
                  <div className="ImageContainer">
                    {Obj.OutFits.map((outfit, index) => (
                      <div className="Card">
                        <OutfitCard outfit={outfit} id={index} />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </>
        ))}
      </div>

      <div className="QueryHolder">
        <button className="NewButton" onClick={handleSubmit}>
          <img src={broom} className="BroomImage" alt="Broom" />
        </button>
        <form>
          <div className="ChatContainer">
            <textarea
              className="PromptText"
              placeholder="What outfit do you want?"
              value={outfitText}
              onChange={handleOutfitTextChange}
              id="fname"
              onInput={handleTextareaInput}
              name="fname"
              onKeyDown={handleTextAreaKeyDown}
              style={{ width: "100%", height: "auto" }}
              cols={1000}
              // rows={1}
            />
          </div>
        </form>
        <button className="NewButton" onClick={clearChat}>
          <img src={send} className="BroomImage" alt="Send Message" />
        </button>
      </div>
    </div>
  );
}

export default App;
