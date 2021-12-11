import React, { useState, useContext } from "react";
import {
  ActionSetData,
  ActionGetGatheringDataInfo,
  ActionAppendData,
} from "../../actions/Action";
import { Context } from "../../../Store";
import { SET_FLOW } from "../../actions/types";
import Table from "../../layout/Table";
import Snackbar from "../../common/MySnackbar";

function InsertData({ id }) {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  function InsertDataReq() {
    const data = new FormData();
    data.append(
      "trainData",
      document.getElementById("formFile_TrainData").files[0]
    );
    data.append(
      "addTimeCol",
      document.getElementById("formTimeCol_TrainData").checked
    );

    ActionSetData(id, data)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
        dispatch({ type: SET_FLOW, payload: data });
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  }

  const form = (
    <form>
      <div className="form-group text-right">
        <label htmlFor="formFile_TrainData">
          داده های خود را به صورت CSV در این جا آپلود کنید
        </label>
        <input
          type="file"
          className="form-control-file"
          id="formFile_TrainData"
        />

        <div className="form-check" dir="ltr">
          <input
            className="form-check-input"
            type="checkbox"
            value=""
            id="formTimeCol_TrainData"
          />
          <label className="form-check-label" htmlFor="formTimeCol_TrainData">
            ایجاد ستون زمان به داده ها
          </label>
        </div>

        <button
          type="button"
          className="btn btn-primary"
          onClick={InsertDataReq}
        >
          ارسال
        </button>
        <Snackbar
          open={!!error}
          onClose={() => setError("")}
          message={error}
          variant="error"
        />
      </div>
    </form>
  );

  return form;
}

function AppendData({ id }) {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  function InsertDataReq() {
    const data = new FormData();
    data.append(
      "trainData",
      document.getElementById("formFile_TrainDataAppend").files[0]
    );
    data.append(
      "addTimeCol",
      document.getElementById("formTimeCol_TrainDataAppend").checked
    );

    ActionAppendData(id, data)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
        dispatch({ type: SET_FLOW, payload: data });
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  }

  const form = (
    <form>
      <div className="form-group text-center">
        <label htmlFor="formFile_TrainDataAppend">
          برای اضافه کردن به داده های قبلی می توانید داده های جدید را در این
          مکان اضافه کنید.
        </label>
        <input
          type="file"
          className="form-control-file"
          id="formFile_TrainDataAppend"
        />

        <div className="form-check" dir="ltr">
          <input
            className="form-check-input"
            type="checkbox"
            value=""
            id="formTimeCol_TrainDataAppend"
          />
          <label
            className="form-check-label"
            htmlFor="formTimeCol_TrainDataAppend"
          >
            ایجاد ستون زمان به داده ها
          </label>
        </div>

        <button
          type="button"
          className="btn btn-primary"
          onClick={InsertDataReq}
        >
          ارسال
        </button>
        <Snackbar
          open={!!error}
          onClose={() => setError("")}
          message={error}
          variant="error"
        />
      </div>
    </form>
  );

  return form;
}

function ShowData({ id }) {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState(false);

  const [chart, setCart] = useState({ state: "hidden", data: null });

  const showData = () => {
    ActionGetGatheringDataInfo(id)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
        setCart({
          state: "show",
          data: data,
        });
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  };

  const hideData = () => {
    setCart({ state: "hidden", data: null });
  };

  const notShow = (
    <button type="button" onClick={showData} className="btn btn-primary">
      مشاهده ی جدول
    </button>
  );

  const show = (
    <>
      <button type="button pl-5" onClick={showData} className="btn btn-primary">
        <i class="bi bi-arrow-repeat"></i>
      </button>
      <button type="button" onClick={hideData} className="btn btn-primary">
        مخفی کردن جدول
      </button>
      <Table df={chart["data"]} />
      <Snackbar
        open={error}
        onClose={() => setError(false)}
        message="خطا در ورود!"
        variant="error"
      />
    </>
  );

  return chart["state"] == "hidden" ? notShow : show;
}

function GatheringData() {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  return (
    <div className="container p-2">
      <InsertData id={flow.id} />

      <AppendData id={flow.id} />

      <ShowData id={flow.id} />
    </div>
  );
}

export default GatheringData;
