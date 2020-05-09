model SlewRateTest
  Modelica.Blocks.Continuous.Integrator pos_smoothed_1(initType = Modelica.Blocks.Types.Init.InitialOutput, k = 0.01986, y(fixed = false), y_start = 22) annotation(
    Placement(visible = true, transformation(extent = {{72, -10}, {92, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.Integrator pos_smoothed_2(initType = Modelica.Blocks.Types.Init.InitialOutput, k = 0.01655, y(fixed = false), y_start = 22) annotation(
    Placement(visible = true, transformation(extent = {{72, 46}, {92, 66}}, rotation = 0)));
  Modelica.Blocks.Nonlinear.SlewRateLimiter limit_a(Rising = 10, Td = 0.0001, initType = Modelica.Blocks.Types.Init.InitialOutput, y_start = 0) annotation(
    Placement(visible = true, transformation(extent = {{32, -10}, {52, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.Der v annotation(
    Placement(visible = true, transformation(extent = {{0, -10}, {20, 10}}, rotation = 0)));
  Modelica.Blocks.Nonlinear.SlewRateLimiter limit_v(Rising = 10, Td = 0.0001, initType = Modelica.Blocks.Types.Init.InitialOutput, y_start = positionStep.offset) annotation(
    Placement(visible = true, transformation(extent = {{-36, -10}, {-16, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Gain Kp(k = 1) annotation(
    Placement(visible = true, transformation(origin = {-52, 0}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Nonlinear.SlewRateLimiter slewRateLimiter1(Rising = 10, Td = 0.0001, initType = Modelica.Blocks.Types.Init.InitialOutput, y_start = 0) annotation(
    Placement(visible = true, transformation(extent = {{32, 46}, {52, 66}}, rotation = 0)));
  Modelica.Blocks.Sources.Step stepdown(height = 3000, offset = 0, startTime = 5) annotation(
    Placement(visible = true, transformation(extent = {{-106, -10}, {-86, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.Der der1 annotation(
    Placement(visible = true, transformation(extent = {{0, 46}, {20, 66}}, rotation = 0)));
  Modelica.Blocks.Nonlinear.SlewRateLimiter slewRateLimiter(Rising = 10, Td = 0.0001, initType = Modelica.Blocks.Types.Init.InitialOutput, y_start = positionStep.offset) annotation(
    Placement(visible = true, transformation(extent = {{-36, 46}, {-16, 66}}, rotation = 0)));
  Modelica.Blocks.Math.Gain gain(k = 1.2) annotation(
    Placement(visible = true, transformation(origin = {-58, 56}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
equation
  connect(limit_a.y, pos_smoothed_1.u) annotation(
    Line(points = {{53, 0}, {70, 0}}, color = {0, 0, 127}));
  connect(v.y, limit_a.u) annotation(
    Line(points = {{21, 0}, {30, 0}}, color = {0, 0, 127}));
  connect(limit_v.y, v.u) annotation(
    Line(points = {{-15, 0}, {-2, 0}}, color = {0, 0, 127}));
  connect(limit_v.u, Kp.y) annotation(
    Line(points = {{-38, 0}, {-45, 0}}, color = {0, 0, 127}));
  connect(slewRateLimiter1.y, pos_smoothed_2.u) annotation(
    Line(points = {{53, 56}, {70, 56}}, color = {0, 0, 127}));
  connect(der1.y, slewRateLimiter1.u) annotation(
    Line(points = {{21, 56}, {30, 56}}, color = {0, 0, 127}));
  connect(slewRateLimiter.y, der1.u) annotation(
    Line(points = {{-15, 56}, {-2, 56}}, color = {0, 0, 127}));
  connect(slewRateLimiter.u, gain.y) annotation(
    Line(points = {{-38, 56}, {-51, 56}}, color = {0, 0, 127}));
  connect(Kp.u, stepdown.y) annotation(
    Line(points = {{-60, 0}, {-84, 0}, {-84, 0}, {-84, 0}}, color = {0, 0, 127}));
  connect(gain.u, stepdown.y) annotation(
    Line(points = {{-66, 56}, {-84, 56}, {-84, 0}, {-84, 0}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end SlewRateTest;
