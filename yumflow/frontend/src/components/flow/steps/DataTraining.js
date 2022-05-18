import React, { useState, useContext } from "react";
import { Context } from "../../../Store";
import { ActionGetAllModels, ActionTrainData } from "../../actions/Action";
import Snackbar from "../../common/MySnackbar";
import { FormGroup, Button, Select, MenuItem } from "@mui/material";
import { Addchart } from "@mui/icons-material";

const DataTraining = () => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];


  const [datainfo, setdatainfo] = useState({ 'test': null, 'train': null });

  const getAllModels = () => {
    ActionGetAllModels(flow.id)
      .then((data) => {
        return data.json();
      })
      .then((data) => {
        if (data.message) throw new Error(data.message);
        console.log(data)
        const options = data.models.map((model) => `<option key=${model.id} value=${model.id}>${model.name}</option>`)
        const sell = document.getElementById("trainSelectormodel")
        sell.innerHTML = options.join('')
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  const sendInfo = () => {

    var select = document.getElementById("trainSelectormodel")
    let id = Number(select.options[select.selectedIndex].value)
    var select = document.getElementById("selectlossFunction")
    let lossfn = select.options[select.selectedIndex].value
    var select = document.getElementById("selectOptimizer")
    let optimizer = select.options[select.selectedIndex].value
    let learning_rate = Number(document.getElementById('learningrateinput').value)

    let batch_size = Number(document.getElementById('batchsizrinput').value)
    let epochs = Number(document.getElementById('epochsinput').value)
    let label_y = document.getElementById('labelyinput').value
    let train_info = { lossfn, optimizer, learning_rate, batch_size, epochs, label_y }

    let data = { id, train_info };
    console.log(data);
    const Addchart = (d) => {
      var xValues = Array.from({length: d.length}, (x, i) => i);
      var yValues = d;

      new Chart("myChart", {
        type: "line",
        data: {
          labels: xValues,
          datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: yValues
          }]
        },
        options: {
          legend: { display: false },
          
        }
      });
    }
    ActionTrainData(flow.id, data)
      .then((data) => {
        return data.json();
      })
      .then((data) => {
        if (data.message) throw new Error(data.message);
        console.log(data)
        Addchart(data['result'])
      })
      .catch((error) => {
        setError(error.message);
      });

  };


  return (
    <>
      <div className="container p-2 text-center">
        <h5>انتخاب مدل</h5>
        <div className="row m-4">
          <select className="form-select" aria-label="Default select example" id="trainSelectormodel">
          </select>
        </div>
        <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getAllModels}>
          گرفتن مدل ها
        </Button>
        <hr />

        <div className="container">
          <div className="row">
            <div className="col-sm border-left">
              <p>loss funtion</p>
              <select className="form-select" aria-label="Default select example" id="selectlossFunction">
                <option value='cross_entropy'>cross entropy</option>
                <option value="mean_absolute_error">mean absolute error</option>
                <option value="mean_square_error">mean square error</option>
                <option value="negative_likelihood">negative likelihood</option>
                <option value="binary_cross_entropy">binary cross entropy</option>
              </select>
            </div>

            <div className="col-sm">
              <p>optimizer</p>
              <select className="form-select" aria-label="Default select example" id="selectOptimizer">
                <option value='adam'>adam</option>
                <option value="SGD">SGD</option>
              </select>
            </div>
            <div className="col-sm">
              <input type="text" className="form-control" placeholder="learning rate" aria-label="learning rate" aria-describedby="basic-addon1" id="learningrateinput" />
              <input type="text" className="form-control" placeholder="batch size" aria-label="batch size" aria-describedby="basic-addon1" id="batchsizrinput" />
              <input type="text" className="form-control" placeholder="epochs" aria-label="epochs" aria-describedby="basic-addon1" id="epochsinput" />
              <input type="text" className="form-control" placeholder="label_y" aria-label="label_y" aria-describedby="basic-addon1" id="labelyinput" />
            </div>
          </div>
        </div>
      </div>
      <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={sendInfo}>آغاز تست</Button>
      <canvas id="myChart"></canvas>

    </>
  );
};

export default DataTraining;
