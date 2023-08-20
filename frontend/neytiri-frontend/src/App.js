import broom from "./broom.png";
import send from "./send.png";
import chatIcon from "./chatIcon.png";
import "./App.css";
import { useEffect, useRef, useState } from "react";
import OutfitCard from "./OutfitCard";
import UserMessage from "./UserMessage";
import LoadingSpinner from "./Loader/Loader";

function App() {
  // var countMessages = 0;
  const [cntMsg, setCntMsg] = useState(0);
  const [outfitText, setOutfitText] = useState("");
  const messagesContainerRef = useRef(null);
  const [outfits, setOutfits] = useState([]);
  const [isSubmitDisabled, setIsSubmitDisabled] = useState(false);
  const [placeholderText, setPlaceholderText] = useState(
    "What outfit are you looking for?"
  );
  // const [chatLog, setChatLog] = useState([
  //   {
  //     IsUser: true,
  //     UserPrompt: "give me tradional outfit",
  //   },
  //   {
  //     IsUser: false,
  //     OutFits: [
  //       {
  //         article_type: "tshirts",
  //         brand_name: "hanes",
  //         color: "black",
  //         gender: "men",
  //         id: 49963,
  //         is_jewellery: false,
  //         master_category: "apparel",
  //         occasion: "casual",
  //         product_display_name: "hanes men black pack of 3 t-shirt",
  //         season: "summer",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/Hanes-Men-Black-Pack-of-3-T-shirt_424f9c9fcdaa10ff2b4fe6b1fa6c18bd_images.jpg",
  //         sub_category: "topwear",
  //       },
  //       {
  //         article_type: "shorts",
  //         brand_name: "hanes",
  //         color: "black",
  //         gender: "men",
  //         id: 49958,
  //         is_jewellery: false,
  //         master_category: "apparel",
  //         occasion: "casual",
  //         product_display_name: "hanes men black athletic 3/4th pants",
  //         season: "summer",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/Hanes-Men-Black-34-Length-Pants_086779a69d95e440744e02cbb33e1581_images.jpg",
  //         sub_category: "bottomwear",
  //       },
  //       {
  //         article_type: "casual_shoes",
  //         brand_name: "converse",
  //         color: "white",
  //         gender: "unisex",
  //         id: 4441,
  //         is_jewellery: false,
  //         master_category: "footwear",
  //         occasion: "none",
  //         product_display_name: "converse unisex canvas hi white shoe",
  //         season: "fall",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/e6c6697fd3aabe8522060801baf0e711_images.jpg",
  //         sub_category: "shoes",
  //       },
  //       {
  //         article_type: "watches",
  //         brand_name: "esprit",
  //         color: "steel",
  //         gender: "men",
  //         id: 10237,
  //         is_jewellery: false,
  //         master_category: "accessories",
  //         occasion: "none",
  //         product_display_name: "esprit men croso black steel watch",
  //         season: "winter",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/cf1675179772f0380d5c44bb797e7df1_images.jpg",
  //         sub_category: "watches",
  //       },
  //     ],
  //   },
  //   {
  //     IsUser: true,
  //     UserPrompt:
  //       "give me tradional outfit in the topwear, ethinic in bottomwear, indian in footwear and accessories",
  //   },
  //   {
  //     IsUser: false,
  //     OutFits: [
  //       {
  //         article_type: "kurtas",
  //         brand_name: "fabindia",
  //         color: "red",
  //         gender: "men",
  //         id: 56691,
  //         is_jewellery: false,
  //         master_category: "apparel",
  //         occasion: "none",
  //         product_display_name: "fabindia men red kurta",
  //         season: "summer",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/Fabindia-Men-Red-Kurta_3cca499449f3df92bca89ccf710216a8_images.jpg",
  //         sub_category: "topwear",
  //       },
  //       {
  //         article_type: "shorts",
  //         brand_name: "adidas",
  //         color: "white",
  //         gender: "men",
  //         id: 2192,
  //         is_jewellery: false,
  //         master_category: "apparel",
  //         occasion: "none",
  //         product_display_name: "adidas men white short",
  //         season: "fall",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/d811aea0d123b18f15fa2a07e134998a_images.jpg",
  //         sub_category: "bottomwear",
  //       },
  //       {
  //         article_type: "sandals",
  //         brand_name: "ganuchi",
  //         color: "brown",
  //         gender: "men",
  //         id: 11937,
  //         is_jewellery: false,
  //         master_category: "footwear",
  //         occasion: "none",
  //         product_display_name: "ganuchi men casual brown sandals",
  //         season: "fall",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/785b8d7da04f23c999c1f424f7c73547_images.jpg",
  //         sub_category: "sandal",
  //       },
  //       {
  //         article_type: "ties",
  //         brand_name: "park_avenue",
  //         color: "blue",
  //         gender: "men",
  //         id: 49744,
  //         is_jewellery: false,
  //         master_category: "accessories",
  //         occasion: "none",
  //         product_display_name: "park avenue men blue tie",
  //         season: "summer",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/a1436f3c892dc55886386d535f73a4ac_images.jpg",
  //         sub_category: "ties",
  //       },
  //     ],
  //   },
  //   {
  //     IsUser: true,
  //     UserPrompt: "bottom wear is boring, give me ethinic ",
  //   },
  //   {
  //     IsUser: false,
  //     OutFits: [
  //       {
  //         article_type: "kurtas",
  //         brand_name: "fabindia",
  //         color: "red",
  //         gender: "men",
  //         id: 56691,
  //         is_jewellery: false,
  //         master_category: "apparel",
  //         occasion: "none",
  //         product_display_name: "fabindia men red kurta",
  //         season: "summer",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/Fabindia-Men-Red-Kurta_3cca499449f3df92bca89ccf710216a8_images.jpg",
  //         sub_category: "topwear",
  //       },
  //       {
  //         article_type: "trousers",
  //         brand_name: "mark_taylor",
  //         color: "black",
  //         gender: "men",
  //         id: 27180,
  //         is_jewellery: false,
  //         master_category: "apparel",
  //         occasion: "none",
  //         product_display_name: "mark taylor men striped black trousers",
  //         season: "summer",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/dcc262870d3b0b66b6c806b18fa3d1bd_images.jpg",
  //         sub_category: "bottomwear",
  //       },
  //       {
  //         article_type: "sandals",
  //         brand_name: "ganuchi",
  //         color: "brown",
  //         gender: "men",
  //         id: 11937,
  //         is_jewellery: false,
  //         master_category: "footwear",
  //         occasion: "none",
  //         product_display_name: "ganuchi men casual brown sandals",
  //         season: "fall",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/785b8d7da04f23c999c1f424f7c73547_images.jpg",
  //         sub_category: "sandal",
  //       },
  //       {
  //         article_type: "ties",
  //         brand_name: "park_avenue",
  //         color: "blue",
  //         gender: "men",
  //         id: 49744,
  //         is_jewellery: false,
  //         master_category: "accessories",
  //         occasion: "none",
  //         product_display_name: "park avenue men blue tie",
  //         season: "summer",
  //         style_image:
  //           "http://assets.myntassets.com/v1/images/style/properties/a1436f3c892dc55886386d535f73a4ac_images.jpg",
  //         sub_category: "ties",
  //       },
  //     ],
  //   },
  // ]);
  const [chatLog, setChatLog] = useState([]);

  useEffect(() => {
    window.addEventListener("beforeunload", clearChat);

    return () => {
      window.removeEventListener("beforeunload", clearChat);
    };
  }, []);

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
    setChatLog([]);
    setOutfitText("");
    setIsSubmitDisabled(false);
    setCntMsg(0);
    setPlaceholderText("What outfit are you looking for?");
    try {
      //http://192.168.248.92:8122/reset_chat
      const response = await fetch("http://localhost:8122/reset_chat");
      if (response.ok) {
        console.log("Chat Cleared");
      } else {
        console.error("Error fetching data:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  // const fakeApiCall = async (currText) => {
  //   // Simulate a delay to mimic network response time
  //   await new Promise((resolve) => setTimeout(resolve, 1000));

  //   const fakeResponse = {
  //     outfit: [
  //       {
  //         IsUser: false,
  //         OutFits: [
  //           {
  //             article_type: "tshirts",
  //             brand_name: "hanes",
  //             color: "black",
  //             gender: "men",
  //             id: 49963,
  //             is_jewellery: false,
  //             master_category: "apparel",
  //             occasion: "casual",
  //             product_display_name: "hanes men black pack of 3 t-shirt",
  //             season: "summer",
  //             style_image:
  //               "http://assets.myntassets.com/v1/images/style/properties/Hanes-Men-Black-Pack-of-3-T-shirt_424f9c9fcdaa10ff2b4fe6b1fa6c18bd_images.jpg",
  //             sub_category: "topwear",
  //           },
  //           {
  //             article_type: "shorts",
  //             brand_name: "hanes",
  //             color: "black",
  //             gender: "men",
  //             id: 49958,
  //             is_jewellery: false,
  //             master_category: "apparel",
  //             occasion: "casual",
  //             product_display_name: "hanes men black athletic 3/4th pants",
  //             season: "summer",
  //             style_image:
  //               "http://assets.myntassets.com/v1/images/style/properties/Hanes-Men-Black-34-Length-Pants_086779a69d95e440744e02cbb33e1581_images.jpg",
  //             sub_category: "bottomwear",
  //           },
  //           {
  //             article_type: "casual_shoes",
  //             brand_name: "converse",
  //             color: "white",
  //             gender: "unisex",
  //             id: 4441,
  //             is_jewellery: false,
  //             master_category: "footwear",
  //             occasion: "none",
  //             product_display_name: "converse unisex canvas hi white shoe",
  //             season: "fall",
  //             style_image:
  //               "http://assets.myntassets.com/v1/images/style/properties/e6c6697fd3aabe8522060801baf0e711_images.jpg",
  //             sub_category: "shoes",
  //           },
  //           {
  //             article_type: "watches",
  //             brand_name: "esprit",
  //             color: "steel",
  //             gender: "men",
  //             id: 10237,
  //             is_jewellery: false,
  //             master_category: "accessories",
  //             occasion: "none",
  //             product_display_name: "esprit men croso black steel watch",
  //             season: "winter",
  //             style_image:
  //               "http://assets.myntassets.com/v1/images/style/properties/cf1675179772f0380d5c44bb797e7df1_images.jpg",
  //             sub_category: "watches",
  //           },
  //         ],
  //       },
  //     ],
  //   };

  //   return fakeResponse;
  // };

  // const handleSubmitFake = async (event) => {
  //   let currCnt = cntMsg;
  //   currCnt += 1;
  //   console.log("curr cnt is ", currCnt);
  //   setIsSubmitDisabled(true);
  //   setPlaceholderText("Query in progress...");
  //   if (currCnt <= 5) {
  //     event.preventDefault();
  //     const currText = outfitText;
  //     setOutfitText("");
  //     const currData = [
  //       {
  //         IsUser: true,
  //         UserPrompt: currText,
  //       },
  //       {
  //         IsUser: false,
  //         OutFits: [],
  //       },
  //     ];
  //     setChatLog((prevChats) => [...prevChats, ...currData]);
  //     // setTimeout(() => {}, 1000);
  //     try {
  //       // Simulate the API call
  //       const data = await fakeApiCall(currText);

  //       const currData = [
  //         {
  //           IsUser: false,
  //           OutFits: data.outfit,
  //         },
  //       ];
  //       setChatLog((prevChats) => {
  //         // Create a copy of the previous array
  //         const newChatLog = [...prevChats];

  //         // Remove the last item from the copy
  //         newChatLog.pop();

  //         // Add the new item (currData) to the end
  //         newChatLog.push(...currData);

  //         return newChatLog;
  //       });
  //       setIsSubmitDisabled(false);
  //       setOutfits(data.outfit);
  //       setCntMsg(currCnt);
  //       setPlaceholderText("What outfit are you looking for?");
  //       console.log("Outfit search successful!");
  //     } catch (error) {
  //       console.error("Error:", error);
  //     }
  //   } else {
  //     event.preventDefault();
  //     // const currText = outfitText;
  //     setOutfitText("");

  //     const currData = [
  //       {
  //         IsUser: false,
  //         OutFits: [],
  //       },
  //     ];
  //     setChatLog((prevChats) => [...prevChats, ...currData]);
  //     setIsSubmitDisabled(true);
  //     setPlaceholderText(
  //       "Limit Reached. Clear chat or refresh the page to continue!"
  //     );
  //   }
  // };

  const handleSubmit = async (event) => {
    let currCnt = cntMsg;
    currCnt += 1;
    console.log("curr cnt is ", currCnt);
    setIsSubmitDisabled(true);
    setPlaceholderText("Query in progress...");
    if (currCnt <= 7) {
      event.preventDefault();
      const currText = outfitText;
      setOutfitText("");
      const currData = [
        {
          IsUser: true,
          UserPrompt: currText,
        },
        {
          IsUser: false,
          OutFits: [],
        },
      ];
      setChatLog((prevChats) => [...prevChats, ...currData]);
      const endpoint = "http://localhost:8122/get_outfit"; // Replace with your actual endpoint URL

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            credentials: "include",
          },
          body: JSON.stringify({ user_prompt: currText }),
        });

        if (response.status === 200) {
          // Handle successful response
          const data = await response.json();
          const currData = [
            {
              IsUser: false,
              OutFits: data.outfit,
            },
          ];
          setChatLog((prevChats) => {
            // Create a copy of the previous array
            const newChatLog = [...prevChats];

            // Remove the last item from the copy
            newChatLog.pop();

            // Add the new item (currData) to the end
            newChatLog.push(...currData);

            return newChatLog;
          });
          setIsSubmitDisabled(false);
          setOutfits(data.outfit);
          setCntMsg(currCnt);
          setPlaceholderText("What outfit are you looking for?");

          console.log("Outfit search successful!");
        } else {
          setIsSubmitDisabled(false);
          setChatLog((prevChats) => {
            // Create a copy of the previous array
            const newChatLog = [...prevChats];

            // Remove the last item from the copy
            newChatLog.pop();

            // Add the new item (currData) to the end

            return newChatLog;
          });
          setCntMsg(currCnt);
          setPlaceholderText(
            "I am sorry can't continue. I am still learning so I appreciate your understanding, Kindly Refresh"
          );
          console.error("Outfit search failed.");
        }
      } catch (error) {
        setIsSubmitDisabled(false);
        setCntMsg(currCnt);
        setPlaceholderText(
          "I am sorry can't continue. I am still learning so I appreciate your understanding, Kindly Refresh"
        );
        console.error("Error:", error);
      }
    } else {
      event.preventDefault();
      // const currText = outfitText;
      setOutfitText("");
      const endpoint = "http://localhost:8122/get_outfit";
      const currData = [
        {
          IsUser: false,
          OutFits: [],
        },
      ];
      setChatLog((prevChats) => [...prevChats, ...currData]);
      setIsSubmitDisabled(true);
      setPlaceholderText(
        "Limit Reached. Clear chat or refresh the page to continue!"
      );
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
      <h2 className="WelcomeText">Neytiri: A GenAI Outfit Generator!</h2>
      <hr className="HorizotalLine" />
      <div className="Container ">
        {chatLog.map((Obj, index) => (
          <>
            {Obj.IsUser ? (
              <div className="PrevSearchText">
                <UserMessage message={Obj.UserPrompt} />
              </div>
            ) : (
              <div className="ImageContainer">
                {Obj.OutFits && Obj.OutFits.length === 0 ? (
                  <>
                    {cntMsg >= 7 ? (
                      <div className="Card2">
                        Sorry, You have reached the free tier chat message limit
                        of this conversation, Kindly clear the chat or upgrade
                        to a better plan!
                      </div>
                    ) : (
                      <div className="Card2">
                        {" "}
                        Waiting for the response, Hold Up!
                        {isSubmitDisabled ? <LoadingSpinner /> : null}
                      </div>
                    )}
                  </>
                ) : (
                  <div className="ImageContainer">
                    {Obj.OutFits &&
                      Obj.OutFits.map((outfit, index) => (
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
        <button className="NewButton" onClick={clearChat}>
          <img src={broom} className="BroomImage" alt="Broom" />
        </button>
        <form>
          <div className="ChatContainer">
            <textarea
              className="PromptText"
              placeholder={placeholderText}
              value={outfitText}
              onChange={handleOutfitTextChange}
              id="fname"
              onInput={handleTextareaInput}
              name="fname"
              onKeyDown={handleTextAreaKeyDown}
              style={{ width: "100%", height: "auto" }}
              cols={1000}
              disabled={isSubmitDisabled}
              // rows={1}
            />
          </div>
        </form>
        <button className="NewButton" onClick={handleSubmit}>
          <img src={send} className="BroomImage" alt="Send Message" />
        </button>
      </div>
    </div>
  );
}

export default App;
