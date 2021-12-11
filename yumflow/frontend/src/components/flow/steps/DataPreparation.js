import React, { useState, useEffect, useContext } from "react";
import { Context } from "../../../Store";
import { ActionPrepareData } from "../../actions/Action";
import Snackbar from "../../common/MySnackbar";

const ChooseRows = ({ Pconstraints }) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [constraints, setConstraints] = useState({ and: [], or: [] });
  Pconstraints.length = 0;
  Pconstraints.push(...constraints["and"]);
  const addConditionAnd = () => {
    let cname = document.getElementById("chooseRowCol").value;
    if (!cname) return;
    let b =
      "1" == document.getElementById("chooseRowColFormCustomSelect").value;
    let c = constraints["or"];
    document.getElementById("ChooseRowsLogicCondition").value = "==";
    document.getElementById("ChooseRowsvalueCondition").value = "";

    setConstraints({
      and: [...constraints["and"], [cname, b, c]],
      or: [],
    });
  };

  const AndConditions = constraints["and"].map((c, i) => (
    <div key={i} className="row align-items-center">
      <div className="m-1">
        <button type="button p-5 m-1" className="btn btn-info" dir="ltr">
          {c[0]}
        </button>
        {c[1] ? (
          <button type="button p-5 m-1" className="btn btn-info" dir="ltr">
            ~
          </button>
        ) : (
          <></>
        )}
      </div>
      <i className="bi bi-arrow-left-short"></i>
      {c[2].map((c, i) => (
        <div key={i}>
          <button type="button p-5 m-1" className="btn btn-success" dir="ltr">
            {c[0]} {c[1]}
          </button>
          <button type="button p-5 m-1" className="btn btn-warning" dir="ltr">
            |
          </button>
        </div>
      ))}
    </div>
  ));

  const addConditionOr = () => {
    let logicCondition = document.getElementById(
      "ChooseRowsLogicCondition"
    ).value;
    let valueCondition = document.getElementById(
      "ChooseRowsvalueCondition"
    ).value;
    if (!valueCondition) return;
    document.getElementById("ChooseRowsLogicCondition").value = "==";
    document.getElementById("ChooseRowsvalueCondition").value = "";
    setConstraints({
      and: constraints["and"],
      or: [...constraints["or"], [logicCondition, valueCondition]],
    });
  };
  const notSavedOrs = constraints["or"].map((c, i) => (
    <div key={i}>
      <button type="button p-5 m-1" className="btn btn-success" dir="ltr">
        {c[0]} {c[1]}
      </button>
      <button type="button p-5 m-1" className="btn btn-warning" dir="ltr">
        |
      </button>
    </div>
  ));

  return (
    <div className="container p-2 shadow-sm text-right">
      <h5>آماده‌سازی سطرها</h5>
      <p>در این قسمت شرط‌هایی که برای انتخاب یک سطر لازم است را وارد کنید</p>
      <div className="container">
        <div className="row align-items-center">
          <div className="col-auto">
            <div className="row">
              <div className="col-7">
                <input
                  className="form-control"
                  id="chooseRowCol"
                  name="chooseRowCol"
                  type="text"
                  placeholder="نام ستون"
                />
              </div>
              <div className="col-5">
                <select
                  className="custom-select mr-sm-2"
                  id="chooseRowColFormCustomSelect"
                >
                  <option defaultValue="0"></option>
                  <option value="1">~</option>
                </select>
              </div>
            </div>
          </div>
          <i className="bi bi-arrow-left-short"></i>
          {notSavedOrs}
          <div className="col-auto ">
            <div className="row">
              <select
                className="custom-select mr-sm-2"
                id="ChooseRowsLogicCondition"
                dir="ltr"
              >
                <option defaultValue="=="> == </option>
                <option value="<"> &gt; </option>
                <option value="!="> != </option>
                <option value=">"> &lt;</option>
                <option value="isin"> is in</option>
                <option value="~isin"> ~is in</option>
              </select>
            </div>
          </div>
          <div className="col-auto my-1" dir="ltr">
            <input
              className="form-control"
              type="text"
              id="ChooseRowsvalueCondition"
              placeholder="'ali', 'hassan', 12.5"
            />
          </div>
          <div className="col-auto" dir="ltr">
            <span className="m-1">
              <button
                type="button p-5 m-1"
                onClick={addConditionAnd}
                className="btn btn-primary"
              >
                <i className="bi bi-plus-square"></i>
              </button>
            </span>
            <span className="m-1">
              <button
                type="button p-5 m-1"
                onClick={addConditionOr}
                className="btn btn-primary"
              >
                or
              </button>
            </span>
          </div>
        </div>
        <div className="row align-items-center">
          <div className="container">{AndConditions}</div>
        </div>
      </div>
    </div>
  );
};

const ChooseCols = ({ Pcols }) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];
  // cols
  const [inputCols, setInputCols] = useState({});

  Pcols.length = 0;
  Pcols.push(inputCols);

  const inputColDiv = Object.keys(inputCols).map((name) => (
    <div className="row justify-center" key={name}>
      <div className="col-3" id="column_inputs">
        <input
          className="form-control"
          id={name}
          name={name}
          type="text"
          placeholder="نام ستون"
        />
      </div>
    </div>
  ));

  const onkeyupCol = (e) => {
    if (e.keyCode === 13) {
      let k = `columninput${Object.keys(inputCols).length + 1}`;
      let v = event.target.value;
      setInputCols({
        ...inputCols,
        [k]: v,
      });
      return false;
    }
  };

  useEffect(() => {
    for (const item in inputCols) {
      document.getElementById(item).value = inputCols[item];
    }
    document.getElementById("columninput0").value = "";
  }, [inputCols]);

  const [statCols, setStatCols] = useState(1);

  const oncheckColChanged = (e) => {
    let a = e.target.id;
    a = a.charAt(a.length - 1);
    a = parseInt(a);
    setStatCols(a);
  };

  return (
    <div className="container p-2 shadow-sm text-right">
      <h5>آماده‌سازی ستون‌ها</h5>

      <div className="form-check" dir="ltr">
        <input
          className="form-check-input"
          type="radio"
          name="radioChooseCol"
          id="radioChooseCol1"
          value="option1"
          onChange={oncheckColChanged}
          defaultChecked={statCols == 1}
        />
        <label className="form-check-label" htmlFor="radioChooseCol1">
          انتخاب تمام ستون‌ها
        </label>
      </div>
      <div className="form-check" dir="ltr">
        <input
          className="form-check-input"
          type="radio"
          name="radioChooseCol"
          id="radioChooseCol2"
          value="option2"
          onChange={oncheckColChanged}
        />
        <label className="form-check-label" htmlFor="radioChooseCol2">
          حذف ستون‌های انتخابی
        </label>
      </div>
      <div className="form-check disabled" dir="ltr">
        <input
          className="form-check-input"
          type="radio"
          name="radioChooseCol"
          id="radioChooseCol3"
          value="option3"
          onChange={oncheckColChanged}
        />
        <label className="form-check-label" htmlFor="radioChooseCol3">
          انتخاب ستون‌ها
        </label>
      </div>
      <div style={{ display: statCols == 1 ? "none" : "block" }}>
        {inputColDiv}
        <div className="row justify-center">
          <div className="col-3" id="column_inputs">
            <input
              className="form-control"
              id="columninput0"
              name="columninput0"
              type="text"
              placeholder="نام ستون"
              onKeyUp={onkeyupCol}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

function DataPreparation() {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  // rows

  const Pconstraints = [];
  const Pcols = [];
  const sendInfo = () => {
    let constraints = Pconstraints;
    let cols = Object.values(Pcols[0]);
    let colFilter = 0;
    if (document.getElementById("radioChooseCol2").checked) {
      colFilter = 1;
    } else if (document.getElementById("radioChooseCol3").checked) {
      colFilter = 2;
    }
    let name = document.getElementById("constraints-name").value;
    let data = { constraints, cols, colFilter, name };
    console.log(data);
    ActionPrepareData(flow.id, data)
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
      <div className="row justify-center">
        <div className="col-6" id="column_inputs">
          <input
            className="form-control"
            id="constraints-name"
            name="constraints-name"
            type="text"
            placeholder="لطفا یک نام برای شروط خود وارد کنید"
          />
        </div>
      </div>
      <ChooseCols Pcols={Pcols} />
      <ChooseRows Pconstraints={Pconstraints} />
      <div className="container p-2 shadow-sm text-right">
        <div className="row" dir="ltr">
          <button type="button" className="btn btn-primary" onClick={sendInfo}>
            ارسال اطلاعات
          </button>
        </div>
      </div>
      <Snackbar
        open={!!error}
        onClose={() => setError("")}
        message={error}
        variant="error"
      />
    </>
  );
}

export default DataPreparation;
