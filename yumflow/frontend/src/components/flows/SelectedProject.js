import React, { useState } from "react";
const URL = 'http://127.0.0.1:8000/api/'
import GatheringData from "./steps/GatheringData";

function SelectedProject({ selectedFlow }) {
    if (selectedFlow == -1) {
        return <p className='col-10'>
            پروژه ای انتخاب نشده است
        </p>
    }
    const [project, setProject] = React.useState(null);
    const getFlow = URL + `flows/${selectedFlow}/`
    React.useEffect(() => {
        fetch(getFlow)
            .then(results => results.json())
            .then(data => {
                setProject(data);
            });
    }, []);

    // https://www.javatpoint.com/machine-learning-life-cycle

    return (
        !project ? <p>loading...</p>
            :
            <div className='col-10'>
                <GatheringData project={project} />
            </div >
    )
}

export default SelectedProject