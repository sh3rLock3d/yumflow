import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../../../Store";
import BrainJsVisualizer from "./BrainJsVisualizer";
import { Button, } from "@mui/material";
import { ActionSetModelHyperParameters } from "../../../actions/Action";

function find_size_of_network(layer) {
    const l = []
    var last = 0
    for (const element of layer) {
        if (element.length != 1) {
            l.push(element[1])
            last = element[2]
        }
    }
    l.push(last)
    if (l.length == 1) {
        return [12, 6, 3, 5]
    }
    return l
}




const BuildNetwork = () => {
    const [state, dispatch] = useContext(Context);

    const flow = state["auth"]["flow"];

    const [layer, setlayer] = useState([]);

    useEffect(() => {

        const net = {
            'inputLookup': 1,
            'outputs': 10,
            'sizes': find_size_of_network(layer)
        }
        console.log(net.sizes)
        const wrapper = document.getElementById('myCanvasWrapper');
        if (wrapper.firstChild) wrapper.removeChild(wrapper.firstChild);
        const visualizer = new BrainJsVisualizer(net, wrapper);
        visualizer.render();
    });

    const addActivationFuntion = () => {
        var select = document.getElementById("selectActicationFunction")
        let choosenActivation = select.options[select.selectedIndex].value
        setlayer([...layer, [choosenActivation]])
    }

    const addLayer = () => {
        let input = document.getElementById('layerininput').value
        let output = document.getElementById('layeroutinput').value
        var select = document.getElementById("selectlayer")
        let chooseLayer = select.options[select.selectedIndex].value
        setlayer([...layer, [chooseLayer, Number(input), Number(output)]])

    }

    const sendInfo = () => {
        
        var select = document.getElementById("modelSelectormodel")
        let id = Number(select.options[select.selectedIndex].value)
        let data = { layer, id};
        console.log(data);
        ActionSetModelHyperParameters(flow.id, data)
            .then((data) => {
                return data.json();
            })
            .then((data) => {
                if (data.message) throw new Error(data.message);
                console.log(data)
            })
            .catch((error) => {
                setError(error.message);
            });
            
    };

    const layer_infos = layer.map((l, index) => <li key={index} class="list-group-item">{l.join('-')}</li>)
    return (
        <>
            <h5>ساخت شبکه ی عصبی</h5>
            <hr />
            <ul className="list-group m-5">
                {layer_infos}
            </ul>
            <div className="container">
                <div className="row">
                    <div className="col-sm border-left">
                        <select className="form-select" aria-label="Default select example" id="selectActicationFunction">
                            <option value='relu_function'>relu function</option>
                            <option value="sigmoid_function">sigmoid function</option>
                            <option value="soft_max">soft max</option>
                            <option value="tanh">tanh</option>
                        </select>
                        <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={addActivationFuntion}>اضافه کردن Activation function</Button>
                    </div>

                    <div className="col-sm">
                        <input type="text" className="form-control" placeholder="لایه ورودی" aria-label="لایه ورودی" aria-describedby="basic-addon1" id="layerininput" />
                        <input type="text" className="form-control" placeholder="لایه خروجی" aria-label="لایه خروجی" aria-describedby="basic-addon1" id="layeroutinput" />
                    </div>
                    <div className="col-sm">
                        <select className="form-select" aria-label="Default select example" id="selectlayer">
                            <option value='linear'>linear</option>
                            <option value="conv">convolutional</option>
                        </select>
                        <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={addLayer}>اضافه کردن لایه</Button>
                    </div>
                </div>
            </div>

            <hr />
            <div>
                <div id='myCanvasWrapper'>
                </div>
            </div>

            <Button
                    variant="contained"
                    color="success"
                    style={{ width: "100%", maxWidth: "300px" }}
                    onClick={sendInfo}
                >
                    ساخت شبکه
                </Button>
        </>
    )
};

export default BuildNetwork;
