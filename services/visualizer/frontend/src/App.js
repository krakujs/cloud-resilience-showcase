import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Row, Col, Card, Navbar, Nav } from 'react-bootstrap';
import ResourceTree from './components/ResourceTree';
import './App.css';

function App() {
  const [resources, setResources] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResources = async () => {
      try {
        // This would be the real backend endpoint in production
        const response = await axios.get('http://localhost:3000/api/resources');
        setResources(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch resources');
        setLoading(false);
        console.error('Error fetching resources:', err);
      }
    };

    fetchResources();
  }, []);

  return (
    <div className="app">
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand href="#home">Infrastructure Visualizer</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link href="#home">Home</Nav.Link>
              <Nav.Link href="#resources">Resources</Nav.Link>
              <Nav.Link href="#about">About</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="mt-4">
        <Row>
          <Col>
            <Card>
              <Card.Header as="h5">GCP Resource Visualization</Card.Header>
              <Card.Body>
                {loading && <p>Loading resources...</p>}
                {error && <p className="text-danger">{error}</p>}
                {resources && (
                  <>
                    <ResourceTree data={resources} />
                  </>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
