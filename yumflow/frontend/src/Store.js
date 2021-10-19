import React, {createContext, useReducer} from "react";
import rootReducer from './reducers';

const auth = {
    token: localStorage.getItem('token'),
    isAuthenticated: null,
    isLoading: false,
    user: null,
};

const initialState = {auth};

const Store = ({children}) => {
    const [state, dispatch] = useReducer(rootReducer, initialState);
    return (
        <Context.Provider value={[state, dispatch]}>
            {children}
        </Context.Provider>
    )
};

export const Context = createContext(initialState);
export default Store;