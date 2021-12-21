import React, { useState, useContext } from "react";
import { Context } from "../../../Store";
import { ActionTrainData, ActionGetAllFlowModels } from "../../actions/Action";
import Snackbar from "../../common/MySnackbar";
import { FormGroup, Button, Select, MenuItem } from "@mui/material";

const DataTraining = () => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];
  const [modelId, setModelId] = useState(undefined);

  const [error, setError] = useState(false);

  const [flowModels, setFlowModels] = useState(undefined);

  if (!flowModels)
    ActionGetAllFlowModels(flow.id)
      .then((data) => data.json())
      .then((data) => {
        if (data.message) throw new Error(data.message);
        setFlowModels(data.models);
      })
      .catch((err) => {
        setError(err.message);
      });

  const sendInfo = () => {
    ActionTrainData(flow.id, { id: modelId })
      .then((data) => data.json())
      .then((data) => {
        if (data.message) throw new Error(data.message);
      })
      .catch((error) => {
        setError(error.message);
      });
  };

  const items = () => {
    if (flowModels)
      return flowModels.map((model) => (
        <MenuItem key={model.id} value={model.id}>
          {model.name || "without name"}
        </MenuItem>
      ));
    else return <></>;
  };

  return (
    <>
      <div className="container p-2 text-center">
        <div className="my-row">
          <Select
            style={{ width: 100 }}
            variant="standard"
            id="flow-models-select"
            defaultValue=""
            onChange={(_, eventData) => {
              setModelId(eventData.props.value);
            }}
          >
            {items()}
          </Select>
        </div>
      </div>
      <div className="container p-2 text-center">
        <FormGroup style={{ alignItems: "center" }}>
          <Button
            variant="contained"
            color="success"
            style={{ width: "100%", maxWidth: "300px" }}
            onClick={sendInfo}
          >
            ساخت مدل
          </Button>
        </FormGroup>

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
