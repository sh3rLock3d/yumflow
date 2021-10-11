import React, { useState } from "react";
import DataPreparation from "./steps/DataPreparation";
import GatheringData from "./steps/GatheringData";


function SelectedProject({ selectedFlow, setSelectedFlow }) {


    if (!selectedFlow) {
        return <p className='col-10'>
            پروژه ای انتخاب نشده است
        </p>
    }

    // https://www.javatpoint.com/machine-learning-life-cycle

    return (
        <div className='col-10 mt-3'>
            <div id="accordion">
                <div className="card">
                    <div className="card-header" id="headingOne">
                        <h1 className="mb-0 text-right">
                            <button className="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                ۱.جمع آوری داده ها
                            </button>
                        </h1>
                    </div>

                    <div id="collapseOne" className="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
                        <GatheringData selectedFlow={selectedFlow} setSelectedFlow={setSelectedFlow}/>
                    </div>
                </div>


                <div className="card">
                    <div className="card-header" id="headingTwo">
                        <h1 className="mb-0 text-right">
                            <button className="btn btn-link" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                                ۲.آماده سازی داده ها
                            </button>
                        </h1>
                    </div>

                    <div id="collapseTwo" className="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
                        <DataPreparation selectedFlow={selectedFlow} setSelectedFlow={setSelectedFlow}/>
                    </div>
                </div>



            </div>
        </div >
    )
}

export default SelectedProject