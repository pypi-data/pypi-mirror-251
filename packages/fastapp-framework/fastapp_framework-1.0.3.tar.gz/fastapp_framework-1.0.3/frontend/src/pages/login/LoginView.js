import { useState } from "react"
import { useCookies } from "react-cookie";

import { getToken } from "./funcs";
import { useQuery } from '../../utils/query'
import { Column, Columns } from "../../components/Columns"
import Outline from "../../components/Outline"

export default function Login(props){
    const query = useQuery();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [, setCookies, ] = useCookies(['fastapp_token']);

    const doLogin = async () => {
        const data = await getToken(username, password)

        if(data !== undefined && 'access_token' in data && 'token_type' in data){
            setCookies("fastapp_token", data);
            if(query.get("redir") !== null){
                window.location.replace(query.get("redir"));
            } else {
                window.location.replace("/");
            }
        } else {
            alert("Login Failure!")
        }
    }

    return(
        <Outline>
            <Columns>
                <Column args={'is-6 is-offset-3'}>
                    <h2 className="title has-text-centered">Fastapp Login</h2>
                    <form className="form" action="/api/v1/auth/token" method="POST">
                        <div className="field">
                            <label className="label has-text-light">Username or Email</label>
                            <p className="control">
                                <input className='input' placeholder='Ex: timmy123' type='text' name="username"
                                    value={username} onChange={(e) => setUsername(e.target.value)}/>
                            </p>
                        </div>
                        <div className="field">
                            <label className="label has-text-light">Password</label>
                            <p className="control">
                                <input className='input' type='password' name="password"
                                    value={password} onChange={(e) => setPassword(e.target.value)}/>
                            </p>            
                        </div>
                        <div className="field">
                            <button className="button mt-4 is-fullwidth is-success" onClick={(e) => {
                                e.preventDefault();
                                doLogin();
                            }}>Login</button>
                        </div>
                    </form>
                </Column>
            </Columns>
        </Outline>
    )
}