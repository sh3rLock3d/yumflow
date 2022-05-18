import React, { useState, useContext } from "react";
import { ActionGetAllModels } from "../../actions/Action";
import { Context } from "../../../Store";
import Snackbar from "../../common/MySnackbar";
import { Button } from "@mui/material";
const CreateModel = () => {
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
                const sell = document.getElementById("modelSelectormodel")
                sell.innerHTML = options.join('')
            })
            .catch((error) => {
                setError(error.message);
            });
    }


    const [error, setError] = useState("");
    return (
        <div className="container p-2 text-center">
            <h5>انتخاب مدل</h5>

            <div className="row m-4">
                <select className="form-select" aria-label="Default select example" id="modelSelectormodel">
                </select>
            </div>

            <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getAllModels}>
                گرفتن مدل ها
            </Button>

            <hr />

            <h5>اطلاعات داده ی تست و آموزش</h5>
            <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getAllModels}> اطلاعات داده ی آموزش </Button>
            <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getAllModels}> اطلاعات داده ی تست </Button>

            <h5>ساخت شبکه ی عصبی</h5>

            



        </div>

    )

};

export default CreateModel;
