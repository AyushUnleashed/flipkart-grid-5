import logo from "./logo.svg";
import broom from "./broom.png";
import "./App.css";

function App() {
  return (
    <div className="App">
      <div className="Container"></div>
      <div className="QueryHolder">
        <button className="NewButton">
          {" "}
          <img src={broom} className="BroomImage" />
          Search!
        </button>
        <form>
          <input
            className="PromptText"
            placeholder="What the outfit you want?"
            type="text"
            id="fname"
            name="fname"
          />
        </form>
      </div>
    </div>
  );
}

export default App;
