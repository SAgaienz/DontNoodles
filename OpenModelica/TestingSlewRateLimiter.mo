model Fuckthis
  Modelica.Blocks.Nonlinear.SlewRateLimiter limit_a(Rising = 0.0001, Td = 0.0001, initType = Modelica.Blocks.Types.Init.InitialOutput, y_start = 0) annotation(
    Placement(visible = true, transformation(extent = {{10, -10}, {30, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.Integrator positionSmoothed(initType = Modelica.Blocks.Types.Init.InitialOutput, k = 2, y_start = positionStep.offset) annotation(
    Placement(visible = true, transformation(extent = {{50, -10}, {70, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.Der v annotation(
    Placement(visible = true, transformation(extent = {{-20, -10}, {0, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Step positionStep(height = 3000, offset = 0, startTime = 5) annotation(
    Placement(visible = true, transformation(extent = {{-80, -10}, {-60, 10}}, rotation = 0)));
  Modelica.Blocks.Nonlinear.SlewRateLimiter limit_v(Rising = 0.0001, Td = 0.0001, initType = Modelica.Blocks.Types.Init.InitialOutput, y_start = positionStep.offset) annotation(
    Placement(visible = true, transformation(extent = {{-50, -10}, {-30, 10}}, rotation = 0)));
equation
  connect(limit_a.y, positionSmoothed.u) annotation(
    Line(points = {{31, 0}, {39.5, 0}, {48, 0}}, color = {0, 0, 127}));
  connect(limit_v.y, v.u) annotation(
    Line(points = {{-29, 0}, {-22, 0}}, color = {0, 0, 127}));
  connect(v.y, limit_a.u) annotation(
    Line(points = {{1, 0}, {8, 0}}, color = {0, 0, 127}));
  connect(positionStep.y, limit_v.u) annotation(
    Line(points = {{-59, 0}, {-52, 0}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end Fuckthis;
