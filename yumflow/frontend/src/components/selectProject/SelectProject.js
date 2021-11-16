import React, { useState, useEffect, useContext } from "react";
import { ActionGetAllFlows, ActionCreateFlow } from '../actions/Action'
import { useHistory } from 'react-router-dom';
import {SET_FLOW} from '../actions/types'
import { Context } from '../../Store'

// https://stackoverflow.com/questions/53219113/where-can-i-make-api-call-with-hooks-in-react
function SelectProject() {
    const [projects, setProjects] = useState(null);
    const [error, setError] = useState(false);
    const [submitError, setSubmitError] = useState(false);

    useEffect(() => {
        ActionGetAllFlows()
            .then(data => {
                setProjects(data);
            })
            .catch((error) => {
                console.error('Error:', error);
                setError(true);
            });
    }, []);

    let history = useHistory()
    const [state, dispatch] = useContext(Context);
    function onFlowClicked(flow) {
        dispatch({type: SET_FLOW, payload: flow});
        history.push(`/flow/${flow.id}`)
    }

    const listItems = !projects ? error ? <p style="color: red;">Error loading prjects!</p> : <p>loading</p> : projects.map((flow) =>
        <div className="row" key={flow.id}>
            <div className="card m-3 text-right col" onClick={() => onFlowClicked(flow)} >
                <div className="card-body">
                    <h5 className="card-title"> {flow.title} </h5>
                    <h6 className="card-subtitle mb-2 text-muted"> {flow.description} </h6>
                    <p className="card-text">
                        ساخته شده در:
                        {new Date(flow.created_at).toLocaleDateString('fa-IR')}
                    </p>
                </div>
            </div>
        </div>
    );

    function handleSubmit(e) {
        e.preventDefault();
        let data = {
            "title": document.getElementById("titleFlowForm").value,
            "description": document.getElementById("descriptionFlowForm").value
        }
        ActionCreateFlow(data)
            .then(data => {

                setProjects([...projects, data])
                console.log(data);
            })
            .catch((error) => {
                console.error('Error:', error);
                setSubmitError(true);
            });
    }

    const newFlowDiv = <div className="row">
        <div className="card m-3 col">
            <div className="card-body text-center">
                <h5 className="card-title"> <i className="bi bi-file-earmark-plus"></i> اضافه کردن پروژه</h5>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="titleFlowForm">نام پروژه</label>
                        <input type="text" className="form-control" id="titleFlowForm" placeholder="عنوان پروژه را وارد کنید" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="descriptionFlowForm">توضیحات</label>
                        <input type="text" className="form-control" id="descriptionFlowForm" aria-describedby="descriptionHelp" placeholder="توضیحات پروژه را وارد کنید" />
                        <small id="descriptionHelp" className="form-text text-muted">نوشتن توضیحات اختیاری است.</small>
                    </div>
                    <button className="btn btn-primary">Submit</button>
                    <Snackbar
                      open={error}
                      onClose={() => setError(false)}
                      message="خطا در ارسال فرم!"
                      variant="error"
                    />
                </form>
            </div>
        </div>
    </div>

    return (
        <div className="container">
            {listItems}
            {newFlowDiv}
        </div>
    )
}


export default SelectProject
