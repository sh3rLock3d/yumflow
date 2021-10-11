import React, { useState, useEffect } from "react";
import { ActionGetAllFlows, ActionCreateFlow } from '../actions/Action'


// https://stackoverflow.com/questions/53219113/where-can-i-make-api-call-with-hooks-in-react
function AllProjects({ setSelectedFlow }) {
    const [projects, setProjects] = React.useState(null);
    React.useEffect(() => {
        ActionGetAllFlows()
            .then(data => {
                setProjects(data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, []);


    function onFlowClicked(f) {
        setSelectedFlow(f)
    }
    
    const listItems = !projects ? <p>loading</p> : projects.map((flow) =>
        <div className="card m-3 text-right" key={flow.id} onClick={() => onFlowClicked(flow)} >
            <div className="card-body">
                <h5 className="card-title"> {flow.title} </h5>
                <h6 className="card-subtitle mb-2 text-muted"> {flow.description} </h6>
                <p className="card-text">
                    ساخته شده در:
                    {new Date(flow.created_at).toLocaleDateString('fa-IR')}
                </p>
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
                setSelectedFlow(data)
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const newFlowDiv = <div className="card m-3">
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
            </form>
        </div>
    </div>

    return (
        <div className='col-2 bg-light'>
            {listItems}
            {newFlowDiv}
        </div>
    )
}


export default AllProjects
