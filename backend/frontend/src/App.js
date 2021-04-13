import React, { useState, useEffect } from "react";

import { Layout, Menu } from "antd";
import { UserOutlined } from "@ant-design/icons";
import Http from "./http.js";

import "./App.css";
import Fire from "./fire.js";

export const getFires = () => Http.get(`/api/fires/`);

const { SubMenu } = Menu;
const { Header, Content, Sider } = Layout;

const App = () => {
  const [fires, setFires] = useState([]);
  const [selectedFire, setSelectedFire] = useState({});
  const [showAnimation, setAnimationState] = useState(false);

  useEffect(() => {
    setAnimationState(true);

    getFires()
      .then(fires => {
        setFires(fires);
        setSelectedFire(fires[0]);
      })
      .catch(err => {
        console.error(err);
      });
  }, []);

  return (
    <Layout theme="light" style={{ height: "100%" }}>
      <Header className="header">
        <h3>The Fire Project</h3>
        <div className="logo" />
        <Menu theme="light" mode="horizontal" defaultSelectedKeys={["2"]}>
          <Menu.Item key="1"></Menu.Item>
        </Menu>
      </Header>
      <Layout>
        <Sider width={200} className="site-layout-background">
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            defaultOpenKeys={["sub1"]}
            style={{ height: "100%", borderRight: 0 }}
          >
            <SubMenu key="sub1" icon={<UserOutlined />} title="fire detection">
              {fires.map((f, i) => (
                <Menu.Item
                  key={i}
                  onClick={() => {
                    if (
                      selectedFire &&
                      selectedFire.location !== fires[i].location
                    ) {
                      setAnimationState(true);
                      setSelectedFire(fires[i]);
                    }
                  }}
                >
                  {f.location}
                </Menu.Item>
              ))}
            </SubMenu>
          </Menu>
        </Sider>
        <Layout style={{ padding: "0 24px 24px" }}>
          <Content
            className="site-layout-background"
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280
            }}
          >
            {showAnimation ? <Fire /> : ""}
            <img
              className="site-layout-background"
              src={selectedFire.url}
              sizes="(max-width: 500px) 500px, 800px"
              style={{
                display: "block",
                marginLeft: "auto",
                marginRight: "auto",
                width: "75%",
                height: "75%",
                marginTop: "100px",
                visibility: showAnimation ? "hidden" : ""
              }}
              onLoad={() => {
                setAnimationState(false);
              }}
            ></img>
            <a
              style={{ float: "right" }}
              href={`https://www.google.com/maps/search/?api=1&query=${selectedFire.longitude},${selectedFire.latitude}`}
            >
              <img
                style={{
                  float: "right",
                  visibility: showAnimation ? "hidden" : ""
                }}
                alt="google-maps"
                src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimg.icons8.com%2Fcolor%2F1600%2Fgoogle-maps.png&f=1&nofb=1"
                width="45"
                height="45"
              />
            </a>
          </Content>
        </Layout>
      </Layout>

      <div style={{ textAlign: "center" }}>
        <p>
          (1) 'Contains modified Copernicus Sentinel data [2021]' - (2)
          'Contains modified Copernicus Service information [2021]'
        </p>
      </div>
    </Layout>
  );
};

export default App;
