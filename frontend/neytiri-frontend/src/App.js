import logo from "./logo.svg";
import broom from "./broom.png";
import chatIcon from "./chatIcon.png";
import "./App.css";

function App() {
  return (
    <div className="App">
      <div className="Container">
        <p class="WelcomeText">
          Welcome to Neytiri: An outfit Avatar Generator!
        </p>
      </div>
      <div className="QueryHolder">
        <button className="NewButton">
          {" "}
          <img src={broom} className="BroomImage" />
          Search!
        </button>
        <form>
          <div className="ChatContainer">
            <img src={chatIcon} className="ChatImage" />
            <input
              className="PromptText"
              placeholder="What the outfit you want?"
              type="text"
              id="fname"
              name="fname"
            />
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
