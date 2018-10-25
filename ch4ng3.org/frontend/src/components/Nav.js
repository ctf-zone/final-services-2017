import React, { Component } from 'react'
import {
  Menu,
  Image,
  Button,
  Container,
  Icon
} from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'
import {
  showModal,
  logout
} from '../actions'
import logo from '../assets/logo.svg'

class Nav extends Component {

  constructor(props) {
    super(props)
    this.handleLogIn = this.handleLogIn.bind(this)
    this.handleLogOut = this.handleLogOut.bind(this)
  }

  handleLogIn(e) {
    const { dispatch } = this.props
    dispatch(showModal('login'))
  }

  handleLogOut(e) {
    const { dispatch } = this.props
    dispatch(logout())
  }

  render() {

    const { userName, isLoggedIn } = this.props

    return (
      <Menu inverted attached>
        <Container>

          <Menu.Item as={Link} to='/'>
            <Image src={logo}/>
          </Menu.Item>

          <Menu.Item as={Link} to='/browse'>
            Browse
          </Menu.Item>

          { isLoggedIn ?
              <Menu.Item as={Link} to='/new'>
                New petition
              </Menu.Item>
              :
              null
          }

          <Menu.Menu position='right'>

            { isLoggedIn ?
                <Menu.Item as={Link} to='/user'>
                  <Icon name='user' />
                  <span>{userName}</span>
                </Menu.Item>
                :
                null
            }

            { isLoggedIn ?
                <Menu.Item>
                  <Button
                    inverted
                    onClick={this.handleLogOut}>
                    Log Out
                  </Button>
                </Menu.Item>
                :
                <Menu.Item>
                  <Button
                    inverted
                    onClick={this.handleLogIn}>
                    Log In
                  </Button>
                </Menu.Item>
            }

          </Menu.Menu>

        </Container>
      </Menu>
    )
  }
}

const mapStateToProps = (state) => {
  const { user } = state
  return {
    userName: user.name,
    isLoggedIn: user.name !== undefined
  }
}

export default connect(mapStateToProps)(Nav)
