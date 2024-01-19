import { useState } from "react";
import { useCookies } from "react-cookie";
import { FaKey } from "react-icons/fa";

import { doAuthFetch } from "../utils/auth";
import { useQuery } from "../utils/query";
import { Column, Columns } from "../components/Columns";
import Outline from "../components/Outline";

export default function ResetPassword(props){
    const [password, setPassword] = useState("");
    const [passwordConf, setPasswordConf] = useState("");
    const passGood = ((password === passwordConf) && password.length > 0);
    const [cookies, , removeCookies] = useCookies(['fastapp_token'])

    let query = useQuery()

    const doReset = async () => {
        let token = query.get("token")
        const resp = await doAuthFetch(
            '/api/v1/auth/user/do-reset-password/',
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    token: token,
                    password: password
                })
            },
            cookies.fastapp_token.access_token,
            removeCookies
        )

        if(resp !== null){
            window.location.replace("/login");
        } else {
            window.alert("Error resetting password!")
        }
    }

    return (
        <Outline>
            <Columns>
                <Column args={"is-4 is-offset-4"}>
                    <h1 className="title has-text-centered">Reset Password</h1>
                    <div className="field">
                        <label className="label has-text-light">Password</label>
                        <div className="control has-icons-left">
                            <input className={`input ${passGood ? 'is-success' : 'is-danger'}`} type="password" value={password} onChange={(e) => {
                                e.preventDefault();
                                setPassword(e.target.value);
                            }}></input>
                            <span className="icon is-small is-left">
                                <FaKey />
                            </span>
                        </div>
                    </div>

                    <div className="field">
                        <label className="label has-text-light">Confirm Password</label>
                        <div className="control has-icons-left">
                            <input className={`input ${passGood ? 'is-success' : 'is-danger'}`} type="password" value={passwordConf} onChange={(e) => {
                                e.preventDefault();
                                setPasswordConf(e.target.value);
                            }}></input>
                            <span className="icon is-small is-left">
                                <FaKey />
                            </span>
                            {/* <span className="icon is-small is-right">
                                <i className="fas fa-exclamation-triangle"></i>
                            </span> */}
                        </div>
                        {!passGood && <p className="help is-danger">Passwords do not match or empty</p>}
                    </div>
                    <br></br>
                    <button className="button is-fullwidth is-link" disabled={!passGood} onClick={()=>doReset()}>Reset</button>
                </Column>
            </Columns>
        </Outline>
    )
}