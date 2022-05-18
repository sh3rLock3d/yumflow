import React, { useState, useContext } from "react";
import { Context } from "../../../Store";
import { ActionGetAllModels, ActionTestData } from "../../actions/Action";
import Snackbar from "../../common/MySnackbar";
import { FormGroup, Button, Select, MenuItem } from "@mui/material";
import { Addchart } from "@mui/icons-material";

const DataTesting = () => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const getAllModels = () => {
    ActionGetAllModels(flow.id)
      .then((data) => {
        return data.json();
      })
      .then((data) => {
        if (data.message) throw new Error(data.message);
        console.log(data)
        const options = data.models.map((model) => `<option key=${model.id} value=${model.id}>${model.name}</option>`)
        const sell = document.getElementById("testSelectormodel")
        sell.innerHTML = options.join('')
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  const sendInfo = () => {

    var select = document.getElementById("testSelectormodel")
    let id = Number(select.options[select.selectedIndex].value)
    var select = document.getElementById("selectlossFunctiontest")
    let lossfn = select.options[select.selectedIndex].value
    
    
    let batch_size = Number(document.getElementById('batchsizrinputtest').value)
    
    let label_y = document.getElementById('labelyinputtest').value
    
    let test_info = { lossfn, batch_size, label_y }

    let data = { id, train_info };
    console.log(data);
    ActionTestData(flow.id, data)
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


  return (
    <>
      <div className="container p-2 text-center">
        <h5>انتخاب مدل</h5>
        <div className="row m-4">
          <select className="form-select" aria-label="Default select example" id="testSelectormodel">
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
              <select className="form-select" aria-label="Default select example" id="selectlossFunctiontest">
                <option value='cross_entropy'>cross entropy</option>
                <option value="mean_absolute_error">mean absolute error</option>
                <option value="mean_square_error">mean square error</option>
                <option value="negative_likelihood">negative likelihood</option>
                <option value="binary_cross_entropy">binary cross entropy</option>
              </select>
            </div>

            <div className="col-sm">
              
              <input type="text" className="form-control" placeholder="batch size" aria-label="batch size" aria-describedby="basic-addon1" id="batchsizrinputtest" />
              <input type="text" className="form-control" placeholder="label_y" aria-label="label_y" aria-describedby="basic-addon1" id="labelyinputtest" />
            </div>
          </div>
        </div>
      </div>
      <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={sendInfo}>آغاز تست</Button>

    </>
  );
};

export default DataTesting;
