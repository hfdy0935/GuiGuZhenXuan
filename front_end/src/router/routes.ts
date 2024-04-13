import _404 from './routes/404'
import acl from './routes/acl'
import home from './routes/home'
import login from './routes/login'
import product from './routes/product'
import screen from './routes/screen'


export const constRoutes = [...login,...home,..._404,...screen]
export const asyncRoutes = [...acl,...product]