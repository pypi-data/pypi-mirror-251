import { useState, useEffect } from 'react';
import { useCookies } from "react-cookie";
import { MdDelete } from "react-icons/md";

import { doAuthFetch } from "../../utils/auth"

export default function Members(props){
    const [users, setUsers] = useState([]);
    const [reload, setReload] = useState(false);
    const [cookies, , removeCookies] = useCookies(['fastapp_token']);

    const doDeleteUser = async (username) => {
        if(cookies.fastapp_token === undefined){
            window.location.replace("/login");
        }

        const resp = await doAuthFetch(
            `/api/v1/auth/user`,
            {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: username
                })
            },
            cookies.fastapp_token.access_token,
            removeCookies, 
        )

        setReload(!reload);
        console.log(resp);
    };

    useEffect(() => {
        const fetchMembers = async () => {
            if(cookies.fastapp_token === undefined){
                window.location.replace("/login");
            }

            const data = await doAuthFetch(
                `/api/v1/auth/users?is_admin=${props.is_admin}`,
                {
                    method: "GET"
                },
                cookies.fastapp_token.access_token,
                removeCookies, 
            )

            if(data === null){
                // TODO: HANDLE ERROR BETTER
                return;
            }
            setUsers(data);
        }

        fetchMembers()
    }, [cookies.fastapp_token, removeCookies, props.is_admin, reload]);

    return (
        <table className="table is-fullwidth has-background-dark is-bordered">
            <thead>
                <tr>
                    <th className='has-text-light'>Username</th>
                    <th className='has-text-light'>Email</th>
                    <th className='has-text-light'>Active</th>
                    <th className='has-text-light'>Admin</th>
                    <th className='has-text-light'>Delete</th>
                </tr>
            </thead>
            <tbody>
                { users.map !== undefined && users.map((value, index) => <tr key={index}>
                    <td className='has-text-light'>{value.name}</td>
                    <td className='has-text-light'>{value.email}</td>
                    <td className='has-text-light'>{value.is_active ? 'Yes': 'No'}</td>
                    <td className='has-text-light'>{value.is_admin ? 'Yes' : 'No'}</td>
                    <th className='has-text-light'>
                        <a href='/user/delete' onClick={(e) => {
                            e.preventDefault();
                            if(window.confirm(`Are you sure you want to delete '${value.name}'`))
                                doDeleteUser(value.name);
                            // DO DELETE
                        }}><MdDelete /></a>
                    </th>
                </tr>)}
            </tbody>
        </table>
    )
}