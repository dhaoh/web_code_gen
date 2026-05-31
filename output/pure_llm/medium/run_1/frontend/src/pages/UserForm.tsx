import { useState, useEffect, FormEvent } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getUser, createUser, updateUser } from '../api'

export default function UserForm() {
  const { id } = useParams()
  const isEdit = Boolean(id)
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '', role: 'student', full_name: '', email: '' })
  const [error, setError] = useState('')

  useEffect(() => {
    if (isEdit) {
      getUser(Number(id)).then(user => {
        setForm({ username: user.username, password: '', role: user.role, full_name: user.full_name, email: user.email })
      }).catch(err => setError(err.message))
    }
  }, [id])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      const payload = {
        username: form.username,
        password: form.password,
        role: form.role,
        full_name: form.full_name,
        email: form.email
      }
      if (isEdit) {
        await updateUser(Number(id), payload)
      } else {
        await createUser(payload)
      }
      navigate('/users')
    } catch (err: any) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h2>{isEdit ? 'Edit User' : 'New User'}</h2>
      <form onSubmit={handleSubmit}>
        <div><label>Username</label><input required value={form.username} onChange={e => setForm({...form, username: e.target.value})} /></div>
        <div><label>Password</label><input type="password" required={!isEdit} value={form.password} onChange={e => setForm({...form, password: e.target.value})} /></div>
        <div><label>Role</label>
          <select value={form.role} onChange={e => setForm({...form, role: e.target.value})}>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div><label>Full Name</label><input required value={form.full_name} onChange={e => setForm({...form, full_name: e.target.value})} /></div>
        <div><label>Email</label><input type="email" required value={form.email} onChange={e => setForm({...form, email: e.target.value})} /></div>
        {error && <div style={{color:'red'}}>{error}</div>}
        <button type="submit">Save</button>
        <button type="button" onClick={() => navigate('/users')}>Cancel</button>
      </form>
    </div>
  )
}