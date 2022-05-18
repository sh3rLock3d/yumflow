import React, { useContext, useEffect} from "react";
import { Context } from "../../../../Store";
import BrainJsVisualizer from "./BrainJsVisualizer";

const BuildNetwork = () => {
    const [state, dispatch] = useContext(Context);
    const flow = state["auth"]["flow"];

    useEffect(() => {
        
        const net = {
            'inputLookup': 1,
            'outputs': 10,
            'sizes': [12,6, 2]
        }
        

        const wrapper = document.getElementById('myCanvasWrapper');
        const visualizer = new BrainJsVisualizer(net, wrapper);
        visualizer.render();
      });

    

    return (
        <>
            <h5>ساخت شبکه ی عصبی</h5>
            <hr />
            <div>
                <div id='myCanvasWrapper'>   
                </div>
            </div>
            
        </>
    )
};

export default BuildNetwork;
