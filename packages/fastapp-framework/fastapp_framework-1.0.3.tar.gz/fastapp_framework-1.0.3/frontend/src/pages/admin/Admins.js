import React, { useState, useEffect } from 'react';
import { useCookies } from "react-cookie";

import { doAuthFetch } from "../../utils/auth"

export default function Admins(props){
    const [users, setUsers] = useState([]);
    const [cookies, , removeCookies] = useCookies(['fastapp_token']);

    useEffect(() => {
        const fetchAdmins = async () => {
            if(cookies.fastapp_token === undefined){
                window.location.replace("/login?redir=/admin");
            }

            const data = await doAuthFetch(
                "/api/v1/auth/users?is_admin=true",
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

        fetchAdmins()
    }, [cookies.fastapp_token, removeCookies]);

    return (
        <table className="table is-fullwidth has-background-dark">
            <thead>
                <tr>
                    <th className='has-text-light'>Username</th>
                    <th className='has-text-light'>Email</th>
                    <th className='has-text-light'>Active</th>
                    <th className='has-text-light'>Admin</th>
                </tr>
            </thead>
            <tbody>
                { users.map !== undefined && users.map((value, index) => <tr key={index}>
                    <td className='has-text-light'>{value.name}</td>
                    <td className='has-text-light'>{value.email}</td>
                    <td className='has-text-light'>{value.is_active ? 'Yes': 'No'}</td>
                    <td className='has-text-light'>{value.is_admin ? 'Yes' : 'No'}</td>
                </tr>)}
            </tbody>
        </table>
    )
}