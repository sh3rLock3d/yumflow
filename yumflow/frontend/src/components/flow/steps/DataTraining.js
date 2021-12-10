import React, { useState, useContext } from "react";
import { Context } from "../../../Store";
import { ActionTrainData } from "../../actions/Action";
import Snackbar from "../../common/MySnackbar";

const DataTraining = () => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState(false);

  const sendInfo = () => {
    let label = document.getElementById("trainLable").value;
    ActionTrainData(flow.id, { label })
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  };

  return (
    <>
      <div className="container p-2 shadow-sm text-right">
        <div className="row justify-center">
          <div className="col-3" id="column_inputs">
            <input
              className="form-control"
              id="trainLable"
              type="text"
              placeholder="نام ستون لیبل"
            />
          </div>
        </div>
      </div>
      <div className="container p-2 shadow-sm text-right">
        <div className="row" dir="ltr">
          <button type="button" className="btn btn-primary" onClick={sendInfo}>
            ساخت مدل
          </button>
        </div>
        <Snackbar
          open={!!error}
          onClose={() => setError("")}
          message={error}
          variant="error"
        />
      </div>
    </>
  );
};

export default DataTraining;
