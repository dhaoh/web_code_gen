import { useEffect, useState } from 'react'
import { User, getUsers, deleteUser } from '../api'
import { useNavigate } from 'react-router-dom'

export default function UserList() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const fetchUsers = async () => {
    try {
      const data = await getUsers()
      setUsers(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchUsers() }, [])

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete user?')) return
    try {
      await deleteUser(id)
      setUsers(users.filter(u => u.id !== id))
    } catch (err: any) {
      setError(err.message)
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  if (users.length === 0) return <div>No users found.</div>

  return (
    <div>
      <h2>Users</h2>
      <button onClick={() => navigate('/users/new')}>New User</button>
      <table>
        <thead>
          <tr><th>ID</th><th>Username</th><th>Role</th><th>Full Name</th><th>Email</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td><td>{u.username}</td><td>{u.role}</td><td>{u.full_name}</td><td>{u.email}</td>
              <td>
                <button onClick={() => navigate(`/users/${u.id}/edit`)}>Edit</button>
                <button onClick={() => handleDelete(u.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}