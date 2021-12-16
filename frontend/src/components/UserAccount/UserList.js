import { URL_PREFIX } from '../../constants/API';
import { icons } from './TableIcons';
import MaterialTable from 'material-table';
import React, { useEffect, useState } from 'react';
import {
    Select,
    MenuItem,
    TextField,
} from "@material-ui/core";

import { BACKEND_SERVER_ERROR } from '../../constants/error';
import {
  USER_ADD_SUCCESS,
  USER_EDIT_SUCCESS,
  USER_DELETE_SUCCESS,
} from '../../constants/successMessage';


/////////////////// 
//   API Calls   //
///////////////////

async function fetchUserList() {
    return fetch(`${URL_PREFIX}user`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      }
      throw response;
    })
    .then(data => data.data)
    .catch(response => { 
      // case when backend server is working, and sent frontend the error message
      if (response.status) {
        return response.json();
      } else {
        // case when backend server is not working fine and didn't send any useful info to frontend
        return BACKEND_SERVER_ERROR;
      }
    })
}

async function updateUser(oldUser, newUser) {
  return fetch(`${URL_PREFIX}user`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "condition": {
            "username": oldUser["username"]
        },
        "data": {
            "username": newUser["username"],
            "email": newUser["email"],
            "role": newUser["role"],
            "fullname": newUser["fullname"],
        }
      })
  })
  .then(response => {
      if (response.ok) {
        return response.json();
      }
      throw response;
  })
  .then(data => data)
  .catch(response => { 
    // case when backend server is working, and sent frontend the error message
    if (response.status) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}

async function deleteUser(user) {
  return fetch(`${URL_PREFIX}user`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user)
  })
  .then(response => {
      if (response.ok) {
        return response.json();
      }
      throw response;
  })
  .then(data => data)
  .catch(response => { 
    // case when backend server is working, and sent frontend the error message
    if (response.status) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}

async function addUser(user) {
return fetch(`${URL_PREFIX}user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user)
  })
  .then(response => {
      if (response.ok) {
        return response.json();
      }
      throw response;
  })
  .then(data => data)
  .catch(response => { 
    // case when backend server is working, and sent frontend the error message
    if (response.status) {
      return response.json();
    } else {
      // case when backend server is not working fine and didn't send any useful info to frontend
      return BACKEND_SERVER_ERROR;
    }
  })
}

///////////////////// 
//   HTML Object   //
/////////////////////

export default function UserList({ setError, token, setSuccess }) {

  const [userListData, setUserListData] = useState();

  // acts as component did mount
  // fetch the data
  useEffect( () => {
    async function fetchData() {
      const response = await fetchUserList();
      if (response.isError){
        setError(response);
      }else{
        setUserListData(response);
      }
    }
    fetchData();
  }, [setUserListData]);

  return (
    <MaterialTable
      data={userListData}
      title="User List"
      icons={icons}
      columns={[{
          title: "Username",
          field: "username",
          validate: rowData => Boolean(rowData.username) ? true: "Fill in the field",
      },
      {
          title: "Password",
          field: "password",
          editable: "onAdd",
          render: rowData => <p>*</p>,
          editComponent: t => (
          <TextField
              type="password"
              value={t.value}
              onChange={e => t.onChange(e.target.value)}
          />),
      },
      {
          title: "Full Name",
          field: "fullname",
          validate: rowData => Boolean(rowData.fullname) ? true: "Fill in the field",
      },
      {
          title: "Email",
          field: "email",
          validate: rowData => Boolean(rowData.email) ? true: "Fill in the field",
      },
      {
          title: "Role",
          field: "role",
          lookup: { "admin": 'Admin', "viewer": 'Viewer', "developer": "Developer" },
          editComponent: x => (
              <Select
              value={x.value}
              onChange={e => {
                x.onChange(e.target.value);
                console.group(e.target.value);
              }}
            >
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="developer">Developer</MenuItem>
              <MenuItem value="viewer">Viewer</MenuItem>
            </Select>
          ),
          validate: rowData => Boolean(rowData.role) ? true: "Fill in the field",
      }]}
      editable={{
        onRowAdd: newData =>
          new Promise((resolve, reject) => {
            setTimeout(() => {
              addUser(newData).then( 
                response => {
                  if (response.isError){
                    setError(response);
                  } else {
                    setUserListData([...userListData, newData])
                    setSuccess(USER_ADD_SUCCESS);
                  }
              });
              resolve();
            }, 1000)
          }),
        onRowUpdate: (newData, oldData) =>
          new Promise((resolve, reject) => {
            setTimeout(() => {
              updateUser(oldData, newData).then(
                response => {
                  if (response.isError){
                    setError(response);
                  }else {
                    const dataUpdate = [...userListData];
                    console.log(oldData)
                    const index = oldData.tableData.id;
                    dataUpdate[index] = newData;
                    setUserListData(dataUpdate);
                    setSuccess(USER_EDIT_SUCCESS);
                  }
              });
              resolve();
            }, 1000)
          }),
        onRowDelete: oldData =>
          new Promise((resolve, reject) => {
            setTimeout(() => {
              deleteUser(oldData).then( 
                response => {
                  if (response.isError){
                    setError(response);
                  }else{
                    const dataDelete = [...userListData];
                    const index = oldData.tableData.id;
                    dataDelete.splice(index, 1);
                    setUserListData(dataDelete);
                    setSuccess(USER_DELETE_SUCCESS);
                  }
              });
              resolve()
            }, 1000)
          })
      }}
  />
  );
}

