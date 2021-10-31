import React, { useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { Context } from '../../Store'
import { ActionGetFlow } from "../actions/Action";
import { SET_FLOW } from '../actions/types'

import GatheringData from "./steps/GatheringData";
import DataPreparation from "./steps/DataPreparation";
import DataTraining from "./steps/DataTraining";
import DataTesting from "./steps/DataTesting";



const Flow = () => {
    const { id } = useParams();

    const [state, dispatch] = useContext(Context);
    const flow = state["auth"]["flow"]
    if (!flow || id != flow.id) {
        ActionGetFlow(id)
            .then(data => {

                dispatch({ type: SET_FLOW, payload: data });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        return <p>loading...</p>
    }



    return (
        <div className='col mt-3'>
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
                        <GatheringData />
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

                    <div id="collapseTwo" className="collapse show" aria-labelledby="headingTwo" data-parent="#accordion">
                        <DataPreparation />
                    </div>
                </div>


                <div className="card">
                    <div className="card-header" id="headingThree">
                        <h1 className="mb-0 text-right">
                            <button className="btn btn-link" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                                ۳. آموزش داده ها
                            </button>
                        </h1>
                    </div>

                    <div id="collapseTwo" className="collapse show" aria-labelledby="headingTwo" data-parent="#accordion">
                        <DataTraining />
                    </div>
                </div>


                <div className="card">
                    <div className="card-header" id="headingThree">
                        <h1 className="mb-0 text-right">
                            <button className="btn btn-link" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                                ۴. تست داده ها
                            </button>
                        </h1>
                    </div>

                    <div id="collapseTwo" className="collapse show" aria-labelledby="headingTwo" data-parent="#accordion">
                        <DataTesting />
                    </div>
                </div>
            </div>
        </div >
    )
}

export default Flow