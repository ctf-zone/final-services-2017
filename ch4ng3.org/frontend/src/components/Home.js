import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Segment, Statistic } from 'semantic-ui-react'
import { getStats } from '../actions'
import './Home.css'

class Home extends Component {

  componentDidMount() {
    const { dispatch } = this.props
    dispatch(getStats())
  }

  render() {

    const { stats } = this.props

    const square = {
      width: 200,
      height: 200
    }

    return (
      <div className='home'>
        <div className='header'>
          <div className='world-map'></div>
          <h1 className='slogan'>The world's platform for change</h1>
        </div>

        { stats !== undefined ?
            <div style={{ display: 'table', borderSpacing: '20px', margin: '50px auto' }}>
              <div style={{ width: 600, display: 'table-row' }}>

                <Segment circular style={ square }>
                  <Statistic color='red'>
                    <Statistic.Value>{ stats.members }</Statistic.Value>
                    <Statistic.Label>Members</Statistic.Label>
                  </Statistic>
                </Segment>

                <Segment circular style={ square }>
                  <Statistic color='red'>
                    <Statistic.Value>{ stats.petitions }</Statistic.Value>
                    <Statistic.Label>Petitions</Statistic.Label>
                  </Statistic>
                </Segment>

                <Segment circular style={ square }>
                  <Statistic color='red'>
                    <Statistic.Value>{ stats.signs }</Statistic.Value>
                    <Statistic.Label>Signs</Statistic.Label>
                  </Statistic>
                </Segment>

              </div>
            </div>
            :
            null
        }
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  const { stats } = state
  return {
    stats
  }
}

export default connect(mapStateToProps)(Home)
