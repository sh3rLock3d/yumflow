import React, { useState, useEffect } from "react";
const URL = 'http://127.0.0.1:8000/api/'


// https://stackoverflow.com/questions/53219113/where-can-i-make-api-call-with-hooks-in-react
function AllProjects({setSelectedFlow}) {
    const [projects, setProjects] = React.useState(null);
    const getAllFlows = URL + 'flows/'
    React.useEffect(() => {
        fetch(getAllFlows)
            .then(results => results.json())
            .then(data => {
                setProjects(data);

            });
    }, []);

    function onFlowClicked(id) {
        setSelectedFlow(id)
    }

    const listItems = !projects ? <p>loading</p> : projects.map((flow) =>
        <div className="card m-3 text-right" key={flow.id} onClick={() => onFlowClicked(flow.id)} >
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

    const createFlow = URL + "flows/"
    function handleSubmit(e) {
        e.preventDefault();
        let data = {
            "title": document.getElementById("titleFlowForm").value,
            "descriptions": document.getElementById("descriptionFlowForm").value
        }
        
        fetch(createFlow, {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                setProjects(null)
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    return (
        <div className='col-2 bg-light'>
            {listItems}

            <div className="card m-3">
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

        </div>
    )
}


export default AllProjects
