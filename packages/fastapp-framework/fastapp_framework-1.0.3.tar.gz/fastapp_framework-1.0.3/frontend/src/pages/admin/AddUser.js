import { useState } from "react";
import { useCookies } from "react-cookie";
import { FaUser, FaEnvelope, FaKey, FaUpload } from 'react-icons/fa'

import { doAuthFetch } from "../../utils/auth";
import { Column, Columns } from "../../components/Columns";
import Popup from "../../components/Popups";

export default function AddUser(props){
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [admin, setAdmin] = useState(false);
    const [active, setActive] = useState(true);

    const [sucActive, setSucActive] = useState(false);
    const [sucMsg, setSucMsg] = useState("");

    const [failActive, setFailActive] = useState(false);
    const [failMsg, setFailMsg] = useState("");
    
    const [fileName, setFileName] = useState("No file selected");
    const [fileType, setFileType] = useState("JSON");

    const [cookies, , removeCookies] = useCookies(['fastapp_token'])

    const clear = () => {
        setName('');
        setEmail('');
        setPassword('');
        setAdmin(false);
        setActive(true);
    }

    const doAddUser = async () => {
        const resp = await doAuthFetch('/api/v1/auth/user/',
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password,
                    is_admin: admin,
                    is_active: active
                })
            },
            cookies.fastapp_token.access_token,
            removeCookies
        )
        
        if(resp !== null){
            clear();

            setSucMsg("User added successfully!")
            setSucActive(true);
            setTimeout(() => {setSucActive(false)}, 5000);
        } else {
            setFailMsg("Failed To Create User!")
            setFailActive(true);
            setTimeout(() => {setFailActive(false)}, 5000);
        }
    }

    const doUploadUsers = async () => {
        var data = new FormData()
        data.append('file', document.getElementById('userAddFile').files[0])
        data.append('filetype', fileType)

        const resp = await doAuthFetch('/api/v1/auth/users/',
            {
                method: "POST",
                body: data
            },
            cookies.fastapp_token.access_token,
            removeCookies
        )

        if(resp !== null){
            clear();

            setSucMsg("Users Uploaded, Check Users Page To Ensure All Users Were Added")
            setSucActive(true);
            setTimeout(() => {setSucActive(false)}, 5000);
        } else {
            setFailMsg("Failed To Upload Users!")
            setFailActive(true);
            setTimeout(() => {setFailActive(false)}, 5000);
        }
    }

    return (
        <div>
            <Columns>
                <Column args={'is-5'}>
                    <p className="subtitle has-text-centered">Manual Add</p>

                    <div className="field">
                        <label className="label has-text-light">Username</label>
                        <div className="control has-icons-left">
                            <input className="input" type="text" placeholder="e.g. timmyt123" value={name} onChange={(e) => {
                                e.preventDefault();
                                setName(e.target.value);
                            }}></input>
                            <span className="icon is-small is-left">
                                <FaUser />
                            </span>
                            {/* <span className="icon is-small is-right">
                                <i className="fas fa-check"></i>
                            </span> */}
                        </div>
                        {/* <p className="help is-success">This username is available</p> */}
                    </div>

                    <div className="field">
                        <label className="label has-text-light">Email</label>
                        <div className="control has-icons-left">
                            <input className="input" type="email" placeholder="e.g. hello@whatsup.com" value={email} onChange={(e) => {
                                e.preventDefault();
                                setEmail(e.target.value);
                            }}></input>
                            <span className="icon is-small is-left">
                                <FaEnvelope />
                            </span>
                            {/* <span className="icon is-small is-right">
                                <i className="fas fa-exclamation-triangle"></i>
                            </span> */}
                        </div>
                        {/* <p className="help is-danger">This email is invalid</p> */}
                    </div>

                    <div className="field">
                        <label className="label has-text-light">Password</label>
                        <div className="control has-icons-left">
                            <input className="input" type="password" value={password} onChange={(e) => {
                                e.preventDefault();
                                setPassword(e.target.value);
                            }}></input>
                            <span className="icon is-small is-left">
                                <FaKey />
                            </span>
                            {/* <span className="icon is-small is-right">
                                <i className="fas fa-exclamation-triangle"></i>
                            </span> */}
                        </div>
                        {/* <p className="help is-danger">This email is invalid</p> */}
                    </div>

                    <div className="field">
                        <div className="control">
                            Admin?
                            <label className="radio ml-2 has-text-light">
                                <input type="radio" name="admin" checked={admin === true} onChange={(e) => {
                                    setAdmin(true);
                                }}></input>
                                Yes
                            </label>
                            <label className="radio has-text-light">
                                <input type="radio" name="admin" checked={admin === false} onChange={(e) => {
                                    setAdmin(false);
                                }}></input>
                                No
                            </label>
                        </div>
                    </div>

                    <div className="field">
                        <div className="control">
                            User Activated?
                            <label className="radio ml-2 has-text-light">
                                <input type="radio" name="activated" checked={active === true} onChange={(e) => {
                                    setActive(true);
                                }}></input>
                                Yes
                            </label>
                            <label className="radio has-text-light">
                                <input type="radio" name="activated" checked={active === false} onChange={(e) => {
                                    setActive(false);
                                }}></input>
                                No
                            </label>
                        </div>
                    </div>

                    <div className="field is-grouped">
                        <div className="control">
                            <button className="button is-link" onClick={() => doAddUser()}>Create</button>
                        </div>
                        <div className="control">
                            <button className="button is-link is-light" onClick={() => clear()}>Cancel</button>
                        </div>
                    </div>
                </Column>
                <Column args={'is-5 is-offset-1'}>
                    <p className="subtitle has-text-centered">Bulk Add</p>
                    <p className="">Add users in bulk by uploading a file specifying the users and details to add</p>
                    <br></br>
                    <div className="file has-name is-fullwidth">
                        <label className="file-label">
                            <input id="userAddFile" className="file-input" type="file" name="userlist" onChange={(e) => {
                                setFileName(e.target.files[0].name)
                            }}></input>
                            <span className="file-cta">
                                <span className="file-icon">
                                    <FaUpload />
                                </span>
                                <span className="file-label">
                                    Choose a file…
                                </span>
                            </span>
                            <span className="file-name">
                                {fileName}
                            </span>
                        </label>
                    </div>
                    <br></br>
                    <div className="field">
                        <div className="control">
                            File Type:
                            <label className="radio ml-2 has-text-light">
                                <input type="radio" name="filetype" checked={fileType === "JSON"} onChange={(e) => {
                                    setFileType("JSON");
                                }}></input>
                                JSON
                            </label>
                            <label className="radio has-text-light">
                                <input type="radio" name="filetype" checked={fileType === "CSV"} onChange={(e) => {
                                    setFileType("CSV");
                                }}></input>
                                CSV
                            </label>
                        </div>
                    </div>
                    <button className="button is-fullwidth is-link" onClick={() => {
                        doUploadUsers();
                    }}>Upload</button>
                </Column>
            </Columns>
            <Popup popupClass={"success-box"} active={sucActive} setActive={setSucActive} message={sucMsg}/>
            <Popup popupClass={"failure-box"} active={failActive} setActive={setFailActive} message={failMsg}/>
        </div>
    )
}