import React, { useState } from "react";

import AllProjects from "./AllProjects";
import SelectedProject from "./SelectedProject";

function Flows() {
    const [selectedFlow, setSelectedFlow] = useState(null)
    return (
        <div className="container-fluid">
            <div className="row">
                <AllProjects setSelectedFlow={setSelectedFlow}/>
                <SelectedProject selectedFlow={selectedFlow} setSelectedFlow={setSelectedFlow} />
            </div>
        </div>
    )
}

export default Flows