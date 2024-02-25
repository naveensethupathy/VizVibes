import axios from "axios";
import { useState } from "react";
import ClipLoader from "react-spinners/ClipLoader";
import MoonLoader from "react-spinners/MoonLoader";
import { saveAs } from 'file-saver'

function App() {
  const [image, updateImage] = useState();
  const [prompt, updatePrompt] = useState();
  const [loading, updateLoading] = useState();

  const generate = async (prompt) => {
    updateLoading(true);
    const result = await axios.get(`http://127.0.0.1:8000/?prompt=${prompt}`);
    updateImage(result.data);
    updateLoading(false);
  };
  const downloadImage = () => {
    saveAs(`data:image/png;base64,${image}`, prompt+'image.jpg') 
  }
  return (
    <div className="App">
      <div>
        <div className="heading">
          <h1>Viz Vibez Image Generator</h1>
        </div>

        <div className="input">
          <input
            placeholder="Enter the prompt"
            value={prompt}
            onChange={(e) => updatePrompt(e.target.value)}
          ></input>
          <button className="btn" onClick={(e) => generate(prompt)}>
            Generate
          </button>
        </div>
        <div className="content">
          <p>
            Introducing our Image Generator, a versatile web application
            designed to streamline image creation for designers, marketers, and
            content creators. With an extensive library spanning diverse
            categories like nature, technology, and business, users can
            effortlessly find the perfect image for any project. 
            
            Our platform
            offers robust customization options, allowing users to add text
            overlays, apply filters, and adjust colors to suit their unique
            needs. Whether for web, print, or social media, our images are
            available in various resolutions and formats, ensuring compatibility
            with any platform. With easy search and filter functionalities,
            licensing clarity, and seamless collaboration tools, our Stock Image
            Generator empowers users to save time, cut costs, and unleash their
            creativity like never before.
            <br>
            </br>
            <button className="dbtn" onClick={(e) => downloadImage()}>Download</button>
          </p>
          
          <div className="image-container">
            {loading ? (
              <MoonLoader
                color="#FFC436"
                loading={loading}
                size={50}
                className="loader"
              />
            ) : (
              <img
                className="image"
                src={
                  image
                    ? `data:image/png;base64,${image}`
                    : "https://picsum.photos/1000"
                }
                alt="img"
              />
            )}
          </div>
          
        </div>
        
      </div>
    </div>
  );
}

export default App;
